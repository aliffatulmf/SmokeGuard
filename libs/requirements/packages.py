import importlib.metadata as metadata
import subprocess
import sys


def check_requirements(packages: list, auto_install: bool = True) -> bool:
    missing = []
    for package in packages:
        try:
            metadata.version(package)
        except metadata.PackageNotFoundError:
            if auto_install:
                missing.append(package)

    if auto_install and len(missing) != 0:
        print(
            f"\033[91mMissing dependencies: {missing}, attempting to install...\033[00m"
        )
        try:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", "--quiet", *missing]
            )
        except subprocess.CalledProcessError as e:
            print(f"Failed to install dependencies: {e}")
            return False

    if not auto_install:
        print(f"Missing dependencies: {missing}")
    return len(missing) == 0
