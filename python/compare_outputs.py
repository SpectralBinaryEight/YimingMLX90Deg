import scipy.io
import pandas as pd
import os
import numpy as np
from scipy.stats import ttest_ind, mannwhitneyu, wilcoxon, ks_2samp, anderson_ksamp, chi2_contingency

def mat_to_csv(mat_file_path, csv_file_path=None):
    """
    Converts a .MAT file to a .CSV file with real and imaginary parts of complex numbers separated.

    Parameters:
    mat_file_path (str): Path to the input .MAT file.
    csv_file_path (str, optional): Path to save the output .CSV file. 
                                   If None, saves the .CSV file in the same location as the .MAT file.

    Returns:
    str: Path to the saved .CSV file.
    """
    if not os.path.exists(mat_file_path):
        raise FileNotFoundError(f"The specified .MAT file does not exist: {mat_file_path}")

    # Load the .MAT file
    mat_data = scipy.io.loadmat(mat_file_path)

    # Remove metadata entries (keys starting with '__')
    mat_data = {key: value for key, value in mat_data.items() if not key.startswith('__')}

    # Extract phase keys and corresponding data
    phases = ['output0', 'output90', 'output180', 'output270']
    rows = []

    for phase, key in enumerate(phases):
        if key in mat_data:
            values = mat_data[key].flatten()  # Flatten to ensure 1D array
            for value in values:
                real_part = value.real if isinstance(value, complex) else value
                imag_part = value.imag if isinstance(value, complex) else 0.0
                rows.append({'Phase': phase * 90, 'Real': real_part, 'Imaginary': imag_part})

    # Convert rows to DataFrame
    df = pd.DataFrame(rows)

    # Save the DataFrame to a CSV file
    if csv_file_path is None:
        csv_file_path = os.path.splitext(mat_file_path)[0] + "_converted.csv"
    df.to_csv(csv_file_path, index=False)

    print(f".MAT file converted and saved to .CSV at: {csv_file_path}")
    return csv_file_path

# Example Usage
mat_to_csv('/Users/colincasey/YimingMLX90Deg/data/Yiming_Hybrid90deg_MtP.mat', '/Users/colincasey/YimingMLX90Deg/data/converted_outputs.csv')

def load_csv_data(csv_file_path):
    return pd.read_csv(csv_file_path)

def calculate_magnitude(df):
    return np.sqrt(df['Real']**2 + df['Imaginary']**2)

def perform_statistical_tests(data1, data2):
    """
    Perform statistical tests on two datasets.
    """
    tests = {
        't-test': ttest_ind,
        'Mann-Whitney U': mannwhitneyu,
        'Wilcoxon': wilcoxon,
        'Kolmogorov-Smirnov': ks_2samp,
        'Anderson-Darling': anderson_ksamp,
    }

    results = {}
    for test_name, test_func in tests.items():
        try:
            if test_name == 'Wilcoxon' and len(data1) != len(data2):
                results[test_name] = ("N/A", "Sample sizes must match for Wilcoxon test")
                continue

            # Perform test
            stat, p_value = test_func(data1, data2)
            results[test_name] = (stat, p_value)

        except Exception as e:
            results[test_name] = (None, f"Error: {e}")

    return results

# Load data from CSV files
csv_file_path1 = '/Users/colincasey/YimingMLX90Deg/data/outputs.csv'
csv_file_path2 = '/Users/colincasey/YimingMLX90Deg/data/converted_outputs.csv'

df1 = load_csv_data(csv_file_path1)
df2 = load_csv_data(csv_file_path2)

# Calculate magnitudes
magnitudes1 = calculate_magnitude(df1).to_numpy()
magnitudes2 = calculate_magnitude(df2).to_numpy()

# Perform statistical tests
results = perform_statistical_tests(magnitudes1, magnitudes2)

# Print results
for test_name, result in results.items():
    stat, p_value = result
    if isinstance(p_value, str):  # Handle errors or special cases
        print(f"{test_name}: {p_value}")
    else:
        print(f"{test_name} statistic: {stat}, p-value: {p_value}")
        if p_value < 0.05:
            print(f"The two datasets are significantly different according to the {test_name} test (p < 0.05).")
        else:
            print(f"The two datasets are not significantly different according to the {test_name} test (p >= 0.05).")
# # Perform a statistical comparison
# # Example: Independent t-test
# stat, p_value = ttest_ind(mat_values, csv_values, equal_var=False)

# print(f"T-test statistic: {stat}")
# print(f"P-value: {p_value}")

# # Interpretation
# if p_value < 0.05:
#     print("The two datasets are significantly different (p < 0.05).")
# else:
#     print("The two datasets are not significantly different (p >= 0.05).")