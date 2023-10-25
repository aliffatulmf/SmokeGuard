import argparse
import socket

from rich.console import Console

from lib.process_handler import define_handler_instance, process_handlers

HEADER = """
███████ ███    ███  ██████  ██   ██ ███████     ██████   ██    ██  █████  ██████  ██████
██      ████  ████ ██    ██ ██  ██  ██          ██       ██    ██ ██   ██ ██   ██ ██   ██
███████ ██ ████ ██ ██    ██ █████   █████       ██   ███ ██    ██ ███████ ██████  ██   ██   Control
     ██ ██  ██  ██ ██    ██ ██  ██  ██          ██    ██ ██    ██ ██   ██ ██   ██ ██   ██   Panel
███████ ██      ██  ██████  ██   ██ ███████      ██████  ████████ ██   ██ ██   ██ ██████    v1.0.0
"""


console = Console()


def is_online() -> bool:
    try:
        socket.create_connection(("1.1.1.1", 443), 2)
        return True
    except OSError as err:
        print(f"OS Error: {err}")
    return False


class Arguments(argparse.ArgumentParser):
    def __init__(self):
        super().__init__(
            prog="control_panel.py",
            description="Control Panel for YOLOv5",
        )

    def store_true(self, *args, **kwargs):
        self.add_argument(*args, **kwargs, action="store_true")

    def store_string(self, *args, **kwargs):
        self.add_argument(*args, **kwargs, default="", type=str)


def define_argument_parser():
    argument = Arguments()
    argument.store_true(
        "-c",
        "--clean",
        help="Delete all __pycache__ directories in the current directory and its subdirectories",
    )
    argument.store_true(
        "-i",
        "--install-required",
        help="Download and install dependencies listed in the YOLOv5 requirements",
    )
    argument.store_true(
        "--reinstall",
        help="Completely remove previous installations of the dependencies and then install them afresh. Should be used along with --install-required flag",
    )
    argument.store_string(
        "--name",
        help="Specify the Environment variable name. This is mandatory if you are using a mamba environment.",
    )
    return argument.parse_args()


def main():
    parsed_arguments = define_argument_parser()
    handler_instance = define_handler_instance(parsed_arguments)
    process_handlers(parsed_arguments, handler_instance)


if __name__ == "__main__":
    console.print(HEADER, style="cyan")
    main()
