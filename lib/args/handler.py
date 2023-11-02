import argparse
import os

from rich.table import Table

from lib.cache import remove_cache
from lib.connection.internet import INet
from lib.dependency import install_requirements
from lib.logger import console
from lib.validation.model import SUPPORTED_FORMATS, validation_model_file


class ArgumentHandler:
    def __init__(self, args: argparse.Namespace):
        self.args = args
        self.inet = INet()

    def process(self):
        # Check the internet connection first
        if not self.inet.is_online():
            console.fatal("You are not connected to the internet.")

        # Handle the install arguments
        if self.args.install_required or self.args.install:
            install_requirements(
                reinstall=getattr(self.args, "reinstall", False),
                names=self.args.install if self.args.install else None,
            )
            return False

        # Handle the supported formats argument
        if self.args.supported_formats:
            self.show_supported_formats()
            return False

        # Handle the clean argument
        if self.args.clean:
            remove_cache(self.args.exclude if self.args.exclude else [])
            return False

        # Handle the model argument
        if not self.args.model:
            console.fatal("Please specify the path to the model file")

        if not os.path.exists(self.args.model):
            console.fatal(f"Model file {self.args.model} not found")

        if not validation_model_file(self.args.model):
            console.fatal(
                f"Model file {self.args.model} is not a valid model file. Renaming the file is not a good idea.",
                stop=False,
            )
            self.show_supported_formats()
            exit(1)

        return True

    def show_supported_formats(self):
        # Use a table to display the supported formats
        table = Table(title="Supported Formats")
        table.add_column("Format", justify="center", style="cyan")
        table.add_column("Model", justify="center", style="cyan")
        for format in SUPPORTED_FORMATS:
            table.add_row(format[0], format[1])

        console.print(table, justify="center")
