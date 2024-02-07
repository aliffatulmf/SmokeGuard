"""
Meta Packets
"""


import socket

def check_online(ip="8.8.8.8", port=80):
    """
    Check if the internet connection is available.

    Args:
        ip (str): The IP address to check.
        port (int): The port to check.

    Returns:
        bool: True if the internet connection is available, False otherwise.
    
    Examples:
        >>> if check_online():
        >>>     print("Connected")
        >>> if not check_online(host="1.1.1.1", port=53):
        >>>     raise("Not Connected")
    """
    try:
        with socket.create_connection((ip, port), timeout=5):
            return True
    except socket.error:
        return False


def _install_with_pip(packages, include_version, dry_run=False):
    """
    Installs a list of packages using pip.

    Args:
        packages (list): A list of package names to install.
        include_version (bool): Whether to include the version in the package name.
        dry_run (bool): Whether to perform a dry run without actually installing the packages.

    Returns:
        None
    """
    import subprocess

    for package in packages:
        if include_version:
            try:
                version = subprocess.check_output(["pip", "show", package], universal_newlines=True).split("\n")[1].split(" ")[1]
            except IndexError:
                version = "unknown"
            if not dry_run:
                print(f"Installing package {package} version {version} with pip...")
                subprocess.check_call(["pip", "install", f"{package}=={version}"])
            else:
                print(f"Dry run: Would install package {package} version {version} with pip...")
        else:
            if not dry_run:
                print(f"Installing package {package} with pip...")
                subprocess.check_call(["pip", "install", package])
            else:
                print(f"Dry run: Would install package {package} with pip...")


def install_packages(packages, include_version=False, dry_run=False):
    """
    Installs a list of packages using either conda or pip.

    This method can selectively install versions of packages, perform a dry run without actual installation,
    and choose between conda and pip for the installation process based on the arguments provided.

    Args:
        packages (list): A list of package names to install.
        include_version (bool, optional): If True, include and clean the version information from the package names. Defaults to False.
        dry_run (bool, optional): If True, perform a dry run without actual installation. Defaults to False.

    Examples:
        >>> install_packages(['numpy', 'pandas'], include_version=True, dry_run=True)
        >>> install_packages(['requests==2.24.0', 'urllib3'], include_version=True)
    """
    if include_version:
        packages = clean_versions(packages)
    
    try:
        _install_with_pip(packages, include_version, dry_run)
    except Exception as e:
        print(f"Error installing packages with pip: {e}")


def clean_versions(packages):
    """
    Cleans the version information from a list of package names.
    
    Args:
        packages (list): A list of package names to clean.
        
    Returns:
        list: A list of package names without version information.
    """
    assert isinstance(packages, list), "Packages must be a list."
    
    cleaned_packages = []
    for package in packages:
        if "==" in package:
            package_name, _ = package.split("==")
            cleaned_packages.append(package_name)
        else:
            cleaned_packages.append(package)

    return cleaned_packages


def is_package_installed(packages):
    """
    Checks if a package is installed. 
    
    Args:
        packages (str): A package name to check.
        
    Returns:
        bool: True if the package is installed, False otherwise.
    """
    try:
        import importlib.util
        spec = importlib.util.find_spec(packages)
    except ModuleNotFoundError:
        return False
    return spec is not None
