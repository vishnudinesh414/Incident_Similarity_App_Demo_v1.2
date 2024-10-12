import subprocess
import os
import sys

def create_virtual_environment(env_path):
    """Create a virtual environment."""
    subprocess.run([sys.executable, '-m', 'venv', env_path], check=True)
    print(f"Virtual environment created at '{env_path}'.")

def install_requirements(env_path):
    """Install required packages from requirements.txt."""
    activate_script = os.path.join(env_path, 'Scripts', 'activate.bat')  # For Windows
    command = f'call "{activate_script}" && pip install -r requirements.txt'
    
    # Run the command in a new shell
    subprocess.run(command, shell=True, check=True)
    print("Requirements installed successfully.")

def download_spacy_model(env_path):
    """Download the SpaCy model in the virtual environment."""
    pip_path = os.path.join(env_path, 'Scripts', 'pip')  # For Windows
    subprocess.run([pip_path, 'install', 'spacy'], check=True)  # Ensure SpaCy is installed
    
    # Use the SpaCy command to download the model
    spacy_path = os.path.join(env_path, 'Scripts', 'python')  # Path to the Python executable in the virtual environment
    subprocess.run([spacy_path, '-m', 'spacy', 'download', 'en_core_web_sm'], check=True)  # Install the model
    print("SpaCy model downloaded successfully.")

def main():
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Set the path for the virtual environment (one level up)
    env_path = os.path.join(current_dir, '..', 'python_env')  # Creates 'python_env' in the parent directory
    
    # Step 1: Create a virtual environment
    create_virtual_environment(env_path)

    # Step 2: Install requirements
    install_requirements(env_path)

    # Step 3: Install SpaCy model
    download_spacy_model(env_path)

if __name__ == "__main__":
    main()