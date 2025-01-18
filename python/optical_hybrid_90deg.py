import numpy as np
import csv

def optical_hybrid_90deg(
    signal_input,
    local_oscillator,
    insertion_loss_signal=0.0,
    insertion_loss_local_oscillator=0.0,
    phase_imbalance_slo=0.0,
    phase_imbalance_iq=0.0,
    insertion_loss_imbalance_i=0.0,
    insertion_loss_imbalance_q=0.0
):
    """
    Simulates a 90-degree Optical Hybrid with given parameters.

    Parameters:
        signal_input (complex): Input optical signal (E-field).
        local_oscillator (complex): Local oscillator signal (E-field).
        insertion_loss_signal (float): Signal input insertion loss in dB.
        insertion_loss_local_oscillator (float): Local oscillator insertion loss in dB.
        phase_imbalance_slo (float): Phase imbalance (signal and local oscillator) in radians.
        phase_imbalance_iq (float): Phase imbalance (I and Q branches) in radians.
        insertion_loss_imbalance_i (float): Insertion loss imbalance for I branch in dB.
        insertion_loss_imbalance_q (float): Insertion loss imbalance for Q branch in dB.

    Returns:
        tuple: A tuple of four complex numbers representing the output signals with 0°, 90°, 180°, and 270° phase differences.
    """
    # Convert dB parameters to linear scale
    IL_signal = 10 ** (-insertion_loss_signal / 10)
    IL_lo = 10 ** (-insertion_loss_local_oscillator / 10)
    Imb_I = 10 ** (-insertion_loss_imbalance_i / 10)
    Imb_Q = 10 ** (-insertion_loss_imbalance_q / 10)

    # Adjust input signals based on insertion loss
    signal_input *= IL_signal
    local_oscillator *= IL_lo

    # Transmission matrix for the ideal case
    T = np.array([
        [1, 1],
        [1, -1],
        [1j, 1j],
        [1j, -1j]
    ])

    # Adjust transmission matrix for phase imbalances
    phase_matrix = np.diag([
        1,
        np.exp(1j * phase_imbalance_slo),
        np.exp(1j * phase_imbalance_iq),
        np.exp(1j * (phase_imbalance_slo + phase_imbalance_iq))
    ])

    # Adjust for insertion loss imbalances
    imbalance_matrix = np.diag([1, Imb_I, Imb_Q, Imb_I * Imb_Q])

    # Combine adjustments into the final transmission matrix
    T_adjusted = imbalance_matrix @ phase_matrix @ T

    # Create input signal vector
    E_in = np.array([signal_input, local_oscillator])

    # Calculate output signals
    E_out = T_adjusted @ E_in

    # Return the outputs with specified phase differences
    return E_out[0], E_out[1], E_out[2], E_out[3]


def save_outputs_to_csv(filename, outputs):
    """
    Saves the output signals to a CSV file.

    Parameters:
        filename (str): The name of the CSV file.
        outputs (tuple): A tuple of four complex numbers representing the output signals.
    """
    with open(filename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Phase', 'Real', 'Imaginary'])
        phases = [0, 90, 180, 270]
        for phase, output in zip(phases, outputs):
            csvwriter.writerow([phase, output.real, output.imag])

# Example usage
signal_input = 1 + 1j  # Example complex signal input
local_oscillator = 1 - 1j  # Example complex local oscillator signal

outputs = optical_hybrid_90deg(
    signal_input,
    local_oscillator,
    insertion_loss_signal=1.0,
    insertion_loss_local_oscillator=0.5,
    phase_imbalance_slo=np.pi / 18,  # 10 degrees in radians
    phase_imbalance_iq=np.pi / 36,   # 5 degrees in radians
    insertion_loss_imbalance_i=0.2,
    insertion_loss_imbalance_q=0.1
)

# print("Outputs with 0°, 90°, 180°, and 270° phase differences:")
# for i, output in enumerate(outputs):
#     print(f"Output {i * 90}°: {output}")

# Save the outputs to a CSV file
save_outputs_to_csv('/Users/colincasey/YimingMLX90Deg/data/outputs.csv', outputs)