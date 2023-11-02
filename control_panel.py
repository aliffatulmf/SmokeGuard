import argparse
import logging

from lib.args.handler import ArgumentHandler
from lib.entry import run
from lib.logger import console

HEADER = """
███████ ███    ███  ██████  ██   ██ ███████      ██████  ██    ██  █████  ██████  ██████
██      ████  ████ ██    ██ ██  ██  ██          ██       ██    ██ ██   ██ ██   ██ ██   ██
███████ ██ ████ ██ ██    ██ █████   █████       ██   ███ ██    ██ ███████ ██████  ██   ██
     ██ ██  ██  ██ ██    ██ ██  ██  ██          ██    ██ ██    ██ ██   ██ ██   ██ ██   ██
███████ ██      ██  ██████  ██   ██ ███████      ██████  ████████ ██   ██ ██   ██ ██████
[italic][bold red]Control Panel[/bold red] [underline]based on[/underline] [bold blue]Ultralytics/YOLOv5[/bold blue][/italic]
"""


class CommandArguments:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            prog="control_panel.py", description="Control Panel for SmokeGuard"
        )
        self.arguments()

    def arguments(self):
        package_group = self.parser.add_argument_group("Cleaning Options")
        package_group.add_argument(
            "--install-required",
            action="store_true",
            help="Downloads and installs the required dependencies",
        )
        package_group.add_argument(
            "--reinstall",
            action="store_true",
            help="Forces the reinstallation of the required dependencies. Should be used in conjunction with the --install-required flag",
        )
        package_group.add_argument(
            "--install",
            nargs="*",
            help="Installs the dependencies manually",
        )

        cache_group = self.parser.add_argument_group("Exclusion Options")
        cache_group.add_argument(
            "-c",
            "--clean",
            action="store_true",
            help="Deletes all __pycache__ directories in the current directory and its subdirectories",
        )
        cache_group.add_argument(
            "-e",
            "--exclude",
            nargs="*",
            help="Excludes the specified directories from cache removal",
        )

        verbose_group = self.parser.add_argument_group("Verbosity Options")
        verbose_group.add_argument(
            "--verbose",
            action="store_true",
            default=False,
            help="Displays verbose output",
        )
        verbose_group.add_argument(
            "--quiet",
            action="store_true",
            help="Hides all output except for errors",
        )

        device_group = self.parser.add_argument_group("Device Options")
        device_group.add_argument(
            "--device",
            type=str,
            choices=["cpu", "cuda", "auto"],
            default="auto",
            help="Specifies the device to use for inference",
        )

        model_group = self.parser.add_argument_group("Model Options")
        model_group.add_argument(
            "--model",
            type=str,
            default="weights/model.pt",
            help="Specifies the path to the model.pt file",
        )
        model_group.add_argument(
            "--supported-formats",
            action="store_true",
            help="Supported model file formats",
        )

        run_group = self.parser.add_argument_group("Running Options")
        run_group.add_argument(
            "-r",
            "--run",
            action="store_true",
            help="Runs the program",
        )

    def parse(self):
        return self.parser.parse_args()


if __name__ == "__main__":
    console.print(HEADER, style="cyan", justify="center")

    # Turn off the global logging
    logging.disable()

    cmd_args = CommandArguments()
    handler = ArgumentHandler(cmd_args.parse())
    if handler.process():
        run(**vars(cmd_args.parse()))
