import subprocess
import sys


def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])


def install_all():
    try:
        with open('requirements.txt') as f:
            packages = f.read().splitlines()
            for package in packages:
                install(package)
        print("All dependencies installed successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == '__main__':
    install_all()