import argparse

from libs.logger import console


class ArgumentGroup:
    def __init__(self, parser: argparse.ArgumentParser):
        self.parser = parser

    def add_arguments(self):
        raise NotImplementedError("add_arguments() must be implemented in the subclass")


class DefaultOptions(ArgumentGroup):
    def add_arguments(self):
        self.parser.add_argument("--run", action="store_true", help="run the program")


class DependencyOptions(ArgumentGroup):
    def add_arguments(self):
        package_group = self.parser.add_argument_group("dependency options")
        package_group.add_argument(
            "--install-required",
            action="store_true",
            help="downloads and installs the required dependencies",
        )
        package_group.add_argument(
            "--reinstall",
            action="store_true",
            help="forces the reinstallation of the required dependencies. should be used in conjunction with the --install-required flag",
        )
        package_group.add_argument(
            "--install",
            nargs="+",
            help="installs the dependencies manually",
        )


class ExclusionOptions(ArgumentGroup):
    def add_arguments(self):
        cache_group = self.parser.add_argument_group("exclusion options")
        cache_group.add_argument(
            "-c",
            "--clean",
            action="store_true",
            help="deletes all __pycache__ directories in the current directory and its subdirectories",
        )
        cache_group.add_argument(
            "-e",
            "--exclude",
            nargs="*",
            default=[],
            help="excludes the specified directories from cache removal",
        )


class VerbosityOptions(ArgumentGroup):
    def add_arguments(self):
        verbose_group = self.parser.add_argument_group("verbosity options")
        verbose_group.add_argument(
            "--verbose",
            action="store_true",
            default=False,
            help="displays verbose output",
        )
        verbose_group.add_argument(
            "--quiet",
            action="store_true",
            default=False,
            help="displays no output",
        )


class ModelOptions(ArgumentGroup):
    def add_arguments(self):
        model_group = self.parser.add_argument_group("model options")
        model_group.add_argument(
            "--model",
            type=str,
            help="specifies the model to use for inference",
        )
        model_group.add_argument(
            "--device",
            type=str,
            choices=["cpu", "cuda", "auto"],
            default="auto",
            help="specifies the device to use for inference",
        )
        model_group.add_argument(
            "--supported-formats",
            action="store_true",
            help="supported model file formats",
        )


class SourceOptions(ArgumentGroup):
    def add_arguments(self):
        source_group = self.parser.add_argument_group("source options")
        source_group.add_argument(
            "--source",
            type=str,
            default="0",
            help="specifies the source to use for inference. can be a webcam index (default 0) or video path",
        )


class CommandArguments:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            prog="control_panel.py",
            # description="Control Panel for SmokeGuard based on ultralytics/YOLOv5",
        )
        self.argument_groups = [
            DefaultOptions(self.parser),
            # DependencyOptions(self.parser),
            ExclusionOptions(self.parser),
            VerbosityOptions(self.parser),
            ModelOptions(self.parser),
            SourceOptions(self.parser),
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
            console.fatal(f"Error parsing arguments: {e}")
