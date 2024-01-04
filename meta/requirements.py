import importlib.metadata
import socket
import subprocess


def check_internet_connection(host="8.8.8.8", port=53, timeout=3):
    try: socket.setdefaulttimeout(timeout); socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port)); return True
    except Exception as ex: print(ex); return False

def install_packages(packages, specific_version):
    for package in packages:
        try:
            if not specific_version and "==" in package: package = package.split("==")[0]
            subprocess.check_call(["python", "-m", "pip", "install", package])
        except subprocess.CalledProcessError as cpe: print(cpe); return False
    return True

def check_requirements(deps, auto=False, specific_version=False, verbose=False):
    missing_packages = []
    for package in deps:
        try:
            pkg_name = package.split("==")[0] if "==" in package else package
            dist = importlib.metadata.distribution(pkg_name)
            if verbose: print(f"{pkg_name} ({dist.version}) is installed.")
        except importlib.metadata.PackageNotFoundError:
            print(f"{package} is NOT installed.")
            missing_packages.append(package)
    if missing_packages and auto:
        if check_internet_connection():
            if not install_packages(missing_packages, specific_version): print(f"Failed to install packages: {', '.join(missing_packages)}")
        else: print("No internet connection. Please check your connection and try again.")
    return bool(missing_packages)