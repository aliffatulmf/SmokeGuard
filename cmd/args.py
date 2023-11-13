import argparse

from libs.logger import console


class ArgumentGroup:
    def __init__(self, parser: argparse.ArgumentParser):
        self.parser = parser

    def add_arguments(self):
        raise NotImplementedError("add_arguments() must be implemented in the subclass")


class DefaultOptions(ArgumentGroup):
    def add_arguments(self):
        self.parser.add_argument("--run", action="store_true", help="Run the program")


class DependencyOptions(ArgumentGroup):
    def add_arguments(self):
        package_group = self.parser.add_argument_group("dependency options")
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
            nargs="+",
            help="Installs the dependencies manually",
        )


class ExclusionOptions(ArgumentGroup):
    def add_arguments(self):
        cache_group = self.parser.add_argument_group("exclusion options")
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


class VerbosityOptions(ArgumentGroup):
    def add_arguments(self):
        verbose_group = self.parser.add_argument_group("verbosity options")
        verbose_group.add_argument(
            "--verbose",
            action="store_true",
            default=False,
            help="Displays verbose output",
        )
        verbose_group.add_argument(
            "--quiet",
            action="store_true",
            default=False,
            help="Displays no output",
        )


class ModelOptions(ArgumentGroup):
    def add_arguments(self):
        model_group = self.parser.add_argument_group("model options")
        model_group.add_argument(
            "--model",
            type=str,
            default="weights/model.pt",
            help="Specifies the model to use for inference",
        )
        model_group.add_argument(
            "--device",
            type=str,
            choices=["cpu", "cuda", "auto"],
            default="auto",
            help="Specifies the device to use for inference",
        )
        model_group.add_argument(
            "--supported-formats",
            action="store_true",
            help="Supported model file formats",
        )


class CommandArguments:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            prog="control_panel.py",
            description="Control Panel for SmokeGuard based on ultralytics/YOLOv5",
        )
        self.argument_groups = [
            DefaultOptions(self.parser),
            DependencyOptions(self.parser),
            ExclusionOptions(self.parser),
            VerbosityOptions(self.parser),
            ModelOptions(self.parser),
        ]

    def add_arguments(self):
        for group in self.argument_groups:
            try:
                group.add_arguments()
            except Exception as e:
                console.error(f"Error adding arguments: {e}")
                return False
        return True

    def validate_arguments(self, args):
        # Add your validation logic here
        # For example, check if certain arguments are not None
        if args.verbose and args.quiet:
            return False

        return True

    def parse(self):
        if not self.add_arguments():
            return None

        try:
            args = self.parser.parse_args()
            if self.validate_arguments(args):
                return args
            else:
                console.error("Invalid arguments")
                return None
        except Exception as e:
            console.error(f"Error parsing arguments: {e}")
            return None
