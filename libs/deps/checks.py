import pkg_resources

from libs.dependency import install_requirements
from libs.logger import console


def check_requirements(dep: list[str]):
    try:
        pkg_resources.require(dep)
    except pkg_resources.DistributionNotFound:
        console.error(f"Missing dependency: {dep}")
        console.info("Attempting to install...")
        install_requirements(names=[dep])
        exit(1)
    except pkg_resources.VersionConflict:
        print(f"Version conflict: {dep}")
        exit(1)
