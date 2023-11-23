import pkgutil
import subprocess
import sys

from libs.logger import VerboseLogger, console
from libs.logger.level import *

PIP_PACKAGES = [
    "gitpython>=3.1.30",
    "matplotlib>=3.3",
    "numpy>=1.22.2",
    "opencv-python>=4.1.1",
    "Pillow>=7.1.2",
    "psutil  ",
    "PyYAML>=5.3.1",
    "requests>=2.23.0",
    "scipy>=1.4.1",
    "thop>=0.1.1  ",
    "torch>=1.8.0  ",
    "torchvision>=0.9.0",
    "tqdm>=4.64.0",
    "ultralytics>=8.0.147",
    "pandas>=1.1.4",
    "seaborn>=0.11.0",
    "setuptools>=65.5.1 ",
    "dill>=0.3.7",
]


class Module:
    def __init__(self):
        pass

    def run_command(self, cmd: list):
        try:
            subprocess.check_call(cmd)
        except subprocess.CalledProcessError as e:
            console.log(f"[bold red][ERROR][/bold red] {e}")
            sys.exit(1)

    def pip_command(self, packages: list[str], reinstall: bool = False):
        cmd = [sys.executable, "-m", "pip", "install", "--quiet"]
        if reinstall:
            cmd.append("--force-reinstall")
        cmd.extend(packages)
        return cmd

    def install_required(self, name: str, reinstall: bool = False):
        pip = self.pip_command(PIP_PACKAGES, reinstall)

        tasks = [
            {
                "log": "[bold green][INSTALL][/bold green] [italic green]PIP PACKAGES[/italic green]",
                "command": pip,
            },
        ]
        with console.status("[bold green]Loading ...[/bold green]") as status:
            while tasks:
                task = tasks.pop(0)
                status.update(task["log"])
                self.run_command(task["command"])


def clean_args(args: list[any]) -> list[any]:
    """Removes empty items within the list if only strings are present."""
    if all(isinstance(arg, str) for arg in args):
        [arg for arg in args if arg]
    return args


def install_requirements(
    names: list[str] = PIP_PACKAGES,
    reinstall: bool = False,
    verbose: bool = False,
):
    log = VerboseLogger(verbose)
    log.print_verbose(INFO, "Installing dependencies ...")

    cleaned_args = clean_args(args=names)
    pip_args = [sys.executable, "-m", "pip", "install"]

    if reinstall:
        log.print_verbose(WARNING, "Force reinstalling dependencies ...")
        pip_args.append("--force-reinstall")

    if verbose:
        pip_args.append("--verbose")
    else:
        pip_args.append("--quiet")

    try:
        pip_args.extend(cleaned_args)

        subprocess.check_call(pip_args)
        log.print_verbose(SUCCESS, "Successfully installed dependencies")
    except subprocess.CalledProcessError as e:
        log.print_verbose(FATAL, f"Error occurred while installing dependencies: {e}")


def is_installed(name: str) -> bool:
    return pkgutil.find_loader(name) is not None
