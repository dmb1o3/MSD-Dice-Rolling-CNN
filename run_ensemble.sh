#!/bin/bash

# Function to check if a command exists
command_exists() {
    command -v "$1" &> /dev/null
}

# Check if Miniconda3 is installed
if [ ! -d "$HOME/miniconda3" ]; then
    echo "Miniconda3 not found. Installing Miniconda3..."

    # Step 1: Download the Miniconda installer
    curl https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh -o ~/miniconda.sh

    # Step 2: Install Miniconda quietly
    bash ~/miniconda.sh -b

    # Step 3: Remove the installer
    rm ~/miniconda.sh

    echo "Miniconda3 installed successfully."
else
    echo "Miniconda3 is already installed."
fi

# Ensure Miniconda is added to the PATH
if ! grep -q 'miniconda3/bin' ~/.bashrc; then
    echo "Adding Miniconda to PATH in ~/.bashrc..."
    printf '\n# Add path to conda\nexport PATH="$HOME/miniconda3/bin:$PATH"\n' >> ~/.bashrc
    source ~/.bashrc
    echo "Miniconda has been added to PATH and ~/.bashrc has been updated."
else
    echo "Miniconda is already in PATH."
fi

# Ensure Miniconda is initialized
source ~/miniconda3/bin/activate

# Check if Python 3.9 environment exists
if ! conda info --envs | grep -q "python39"; then
    echo "Creating a new environment with Python 3.9..."
    conda create -n python39 python=3.9 -y
fi

# Activate the Python 3.9 environment
conda activate python39

# Check if requirements.txt exists
if [ -f "requirements.txt" ]; then
    echo "Installing dependencies from requirements.txt..."
    pip install -r requirements.txt
else
    echo "requirements.txt not found. Please ensure it's in the current directory."
    exit 1
fi

# Run ensemble.py
if [ -f "ensemble.py" ]; then
    echo "Running ensemble.py..."
    python ensemble.py
else
    echo "ensemble.py not found. Please ensure it's in the current directory."
    exit 1
fi

echo "Script completed successfully."
