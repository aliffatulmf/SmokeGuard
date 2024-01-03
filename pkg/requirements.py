import importlib
import importlib.util
import socket
import subprocess


def check_pip():
    try:
        result = subprocess.run(["pip", "--version"], capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False


def check_requirements(packages, auto_install=False, requirements_file=None):
    """
    This function checks whether the packages in the list are installed.

    Args:
      packages: A list of package names.
      auto_install: If True, automatically install missing packages using pip. Defaults to False.
      requirements_file: Path to a requirements.txt file containing additional packages to install.

    Returns:
      True if all packages are installed, False otherwise.
    """
    
    if not check_pip():
        raise Exception("pip is not installed.")

    missing_packages = set()
    for package in packages:
        try:
            importlib.import_module(package)
        except ImportError:
            missing_packages.add(package)

    if missing_packages:
        if auto_install:
            install_command = ["pip", "install"]

            # Install packages from requirements file
            if requirements_file:
                install_command.extend(["-r", requirements_file])

            # Install missing packages
            install_command.extend(list(missing_packages))

            try:
                subprocess.run(install_command, check=True)
            except subprocess.CalledProcessError as e:
                raise Exception(f"Failed to install missing packages: {e}")
            return True
        else:
            # Check for optional packages
            optional_packages = set()
            if requirements_file:
                with open(requirements_file, "r") as f:
                    for line in f.readlines():
                        if line.startswith("#"):
                            continue
                        try:
                            package_name, version = line.split("==")
                        except ValueError:
                            package_name = line.strip()
                        if package_name in missing_packages:
                            missing_packages.remove(package_name)
                            optional_packages.add(f"{package_name} {version}")

            # Raise exception if any packages are missing
            message = f"Missing packages: {', '.join(missing_packages)}"
            if optional_packages:
                message += f"\nOptional packages: {', '.join(optional_packages)}"
            raise Exception(message)

    return True


def is_package_installed(package_name):
    """
    This function checks whether a package is installed.
    """
    spec = importlib.util.find_spec(package_name)
    return spec is not None


def check_internet_connection(host="8.8.8.8", port=53, timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except Exception as ex:
        print(ex)
        return False

def check_and_install(deps, auto_install=False):
    if not check_internet_connection():
        print("Tidak ada koneksi internet. Silakan periksa koneksi Anda dan coba lagi.")
        return False

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
            for package in not_installed:
                subprocess.check_call(["python", "-m", "pip", "install", package])
            return True
        else:
            return False
    else:
        print("Semua paket sudah terpasang.")
        return True
