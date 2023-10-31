import argparse
import logging
import socket

from lib.entry import preprocess, run
from lib.log import Logger

HEADER = """
███████ ███    ███  ██████  ██   ██ ███████      ██████  ██    ██  █████  ██████  ██████
██      ████  ████ ██    ██ ██  ██  ██          ██       ██    ██ ██   ██ ██   ██ ██   ██
███████ ██ ████ ██ ██    ██ █████   █████       ██   ███ ██    ██ ███████ ██████  ██   ██
     ██ ██  ██  ██ ██    ██ ██  ██  ██          ██    ██ ██    ██ ██   ██ ██   ██ ██   ██
███████ ██      ██  ██████  ██   ██ ███████      ██████  ████████ ██   ██ ██   ██ ██████
[italic][bold red]Control Panel[/bold red] [underline]based on[/underline] [bold blue]Ultralytics/YOLOv5[/bold blue][/italic]
"""


console = Logger()
# disable global logging
logging.disable()


def is_online() -> bool:
    try:
        socket.create_connection(("1.1.1.1", 443), 2)
        return True
    except OSError as err:
        console.fatal(f"Error: {err}")
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
        default=False,
        help="Show verbose output",
    )

    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Hide all output except for errors",
    )

    parser.add_argument(
        "--device",
        type=str,
        choices=["cpu", "cuda", "auto"],
        default="auto",
        help="Device to use for inference",
    )

    parser.add_argument(
        "--model",
        type=str,
        required=True,
        default="weights/model.pt",
        help="Path to model.pt file",
    )

    parser.add_argument(
        "-r",
        "--run",
        action="store_true",
        help="Run the program",
    )

    return parser.parse_args()


if __name__ == "__main__":
    console.print(HEADER, style="cyan", justify="center")

    args = define_argument_parser()
    kwargs = vars(args)
    preprocess(args)
    run(**kwargs)
