import subprocess
import sys


def install(package):
    """
    Installs given python package

    :param package: A valid python package
    :return: Nothing
    """
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])


def install_all():
    """
    Will read requirements.txt and install all python packages required

    :return: Nothing
    """
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
