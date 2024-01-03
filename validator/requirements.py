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

def check_requirements(deps, auto_install=False, verbose=False):
    not_installed = []
    for package in deps:
        try:
            dist = importlib.metadata.distribution(package)
            print(f"{package} ({dist.version}) is installed.")
        except importlib.metadata.PackageNotFoundError:
            print(f"{package} is NOT installed.")
            not_installed.append(package)

    if not_installed:
        if auto_install:
            if not check_internet_connection():
                if verbose:
                    print("No internet connection. Please check your connection and try again.")
                return True

            try:
                proc = subprocess.run(["python", "-m", "pip", "install"].extend(not_installed))
                proc.check_returncode()
            except subprocess.CalledProcessError as cpe:
                logging.critical(cpe)
                return True
            return False
        else:
            return True
    else:
        if verbose:
            print("All packages are already installed.")
        return False
