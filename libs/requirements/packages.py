import importlib.metadata as metadata
import subprocess
import sys


def check_requirements(packages: list, auto_install: bool = True) -> bool:
    """
    Checks if the required packages are installed.

    This function checks if the required packages are installed. If a package is not installed and auto_install is True,
    the function attempts to install the package. If the installation fails, the function raises an exception.

    Args:
        packages (list): A list of required packages.
        auto_install (bool): Whether to automatically install missing packages. Default is True.

    Returns:
        bool: True if all required packages are installed, False otherwise.

    Raises:
        Exception: If a package is not installed and cannot be installed.
    """
    missing = []
    for package in packages:
        try:
            metadata.version(package)
        except metadata.PackageNotFoundError:
            missing.append(package)

    if len(missing) != 0:
        if auto_install:
            print(
                f"\033[91mMissing dependencies: {missing}, attempting to install...\033[00m"
            )
            try:
                subprocess.check_call(
                    [sys.executable, "-m", "pip", "install", "--quiet", *missing]
                )
            except subprocess.CalledProcessError as e:
                raise Exception(f"Failed to install dependencies: {e}")
        else:
            raise Exception(
                f"Missing dependencies: {missing}. Please install these packages and try again."
            )
    return True
