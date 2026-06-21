import importlib
import importlib.util
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
                        version = ""
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