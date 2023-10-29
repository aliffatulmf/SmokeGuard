import argparse
import socket

from rich.console import Console

from lib.cache import remove_cache
from lib.dependency import PIP_PACKAGES, install_requirements
from lib.entry import run_gui

HEADER = """
███████ ███    ███  ██████  ██   ██ ███████     ██████   ██    ██  █████  ██████  ██████    Control
██      ████  ████ ██    ██ ██  ██  ██          ██       ██    ██ ██   ██ ██   ██ ██   ██   Panel
███████ ██ ████ ██ ██    ██ █████   █████       ██   ███ ██    ██ ███████ ██████  ██   ██   v1.0.0
     ██ ██  ██  ██ ██    ██ ██  ██  ██          ██    ██ ██    ██ ██   ██ ██   ██ ██   ██
███████ ██      ██  ██████  ██   ██ ███████      ██████  ████████ ██   ██ ██   ██ ██████    YOLOv5
"""


console = Console()


def is_online() -> bool:
    try:
        socket.create_connection(("1.1.1.1", 443), 2)
        return True
    except OSError as err:
        console.log(f"[bold red][ERROR][/bold red] {err}")
        return False


def define_argument_parser():
    parser = argparse.ArgumentParser(
        prog="control_panel.py", description="Control Panel for SmokeGuard"
    )

    parser.add_argument(
        "-c",
        "--clean",
        action="store_true",
        help="Delete all __pycache__ directories in the current directory and its subdirectories",
    )
    parser.add_argument(
        "--install-required",
        action="store_true",
        help="Download and install required dependencies",
    )
    parser.add_argument(
        "--reinstall",
        action="store_true",
        help="Force reinstall required dependencies. Should be used along with --install-required flag",
    )
    parser.add_argument(
        "--install",
        nargs="*",
        help="Install dependencies manually",
    )

    parser.add_argument(
        "-e",
        "--exclude",
        nargs="*",
        help="Exclude directories from cache removal",
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show verbose output",
    )

    parser.add_argument(
        "--device",
        type=str,
        choices=["cpu", "cuda", "auto"],
        default="auto",
        help="Device to use for inference",
    )

    parser.add_argument(
        "-r",
        "--run",
        action="store_true",
        help="Run the program",
    )

    return parser.parse_args()


def run_app():
    args = define_argument_parser()

    if args.clean:
        remove_cache(args.exclude if args.exclude else [], args.verbose)

    if args.install_required:
        if not is_online():
            console.print("[bold red][ERROR][/bold red] No internet connection")
            exit(1)

        install_requirements(PIP_PACKAGES, args.reinstall, args.verbose)

    if args.install:
        if not is_online():
            console.print("[bold red][ERROR][/bold red] No internet connection")
            exit(1)

        install_requirements(args.install, args.reinstall, args.verbose)

    if args.run:
        run_gui()


if __name__ == "__main__":
    console.print(HEADER, style="cyan")
    run_app()
