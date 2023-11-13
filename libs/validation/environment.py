import platform as pf
import struct
import sys

from libs.logger import console


class System:
    WINDOWS = "Windows"
    LINUX = "Linux"
    MACOS = "Darwin"


class Architecture:
    X86 = "32bit"
    X86_64 = "64bit"


class WindowsRelease:
    WINDOWS_7 = "7"
    WINDOWS_8 = "8"
    WINDOWS_8_1 = "8.1"
    WINDOWS_10 = "10"


def python_version(major: int, minor: int, patch: int) -> bool:
    if sys.version_info < (major, minor, patch):
        return False


def os_version(name: str, version: str, arch: str):
    if pf.system() != name:
        console.fatal(f"This program is only compatible with {name} operating systems.")
    if pf.release() != version:
        console.fatal(
            f"This program is only compatible with {name} {version} operating systems."
        )
    if struct.calcsize("P") * 8 != int(arch.replace("bit", "")):
        console.fatal(
            f"This program is only compatible with {name} {version} {arch} operating systems."
        )

    return True
