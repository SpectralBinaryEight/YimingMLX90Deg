# YimingMLX90Deg

    # Create a Python virtual environment
        # Open a terminal and navigate to your project directory
        cd /Users/colincasey/YimingMLX90Deg/python

        # Create a virtual environment named 'venv'
        python3 -m venv venv

        # Activate the virtual environment
        # On macOS and Linux:
        source venv/bin/activate
        # On Windows:
        # venv\Scripts\activate

        # Install required packages from requirements.txt
        pip install -r requirements.txt

        # Run the script
        python optical_hybrid_90deg.py

        # Deactivate the virtual environment when done
        deactivate

    # Create a requirements.txt file
        # List the required packages in a file named `requirements.txt` in your project directory
        numpy
        pandas
        scipy

        # You can generate this file automatically by running:
        pip freeze > requirements.txt