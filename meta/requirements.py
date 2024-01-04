import importlib.metadata
import logging
import socket
import subprocess


def check_internet_connection(host="8.8.8.8", port=53, timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except Exception as ex:
        logging.error(ex)
        return False

def install_packages(packages, specific_version):
    for package in packages:
        try:
            if not specific_version and "==" in package:
                package = package.split("==")[0]
            subprocess.check_call(["python", "-m", "pip", "install", package])
        except subprocess.CalledProcessError as cpe:
            logging.error(cpe)
            return False
    return True

def check_requirements(deps, auto=False, specific_version=False, verbose=False):
    """
    Checks if the required packages are installed.

    Parameters:
    deps (list): A list of package names to check. Can include specific versions (e.g., 'package==1.0.0').
    auto (bool): If True, missing packages will be installed automatically. Defaults to False.
    specific_version (bool): If True, installs the specific version included in the package name. If False, installs the latest version. Defaults to False.
    verbose (bool): If True, prints information about each package. Defaults to False.

    Returns:
    bool: Returns True if there are missing packages, False otherwise.
    """
    missing_packages = []
    for package in deps:
        try:
            pkg_name = package.split("==")[0] if "==" in package else package
            dist = importlib.metadata.distribution(pkg_name)
            if verbose:
                print(f"{pkg_name} ({dist.version}) is installed.")
        except importlib.metadata.PackageNotFoundError:
            print(f"{package} is NOT installed.")
            missing_packages.append(package)

    if missing_packages and auto:
        if check_internet_connection():
            if not install_packages(missing_packages, specific_version):
                print(f"Failed to install packages: {', '.join(missing_packages)}")
        else:
            print("No internet connection. Please check your connection and try again.")

    return bool(missing_packages)