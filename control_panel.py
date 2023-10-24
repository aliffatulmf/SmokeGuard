import argparse
import os
import shutil
import socket
import subprocess
import sys
from functools import partial

import requests


def remove_cache() -> None:
    cache_found = False

    for dirPath, _, _ in os.walk("."):
        if dirPath.endswith("__pycache__"):
            try:
                print("Removing", dirPath)
                shutil.rmtree(dirPath)
                cache_found = True
            except Exception as e:
                print(f"Error occurred while removing cache: {e}")

    if not cache_found:
        print("No cache found")


def is_online() -> bool:
    try:
        socket.create_connection(("1.1.1.1", 443), 2)
        return True
    except OSError as err:
        print(f"OS Error: {err}")
    return False


class Dependency:
    def __init__(self):
        self.url = "https://raw.githubusercontent.com/ultralytics/yolov5/master/requirements.txt"

    def fetch_requirements(self) -> list:
        if not is_online():
            print("You are offline. Please connect to the internet first.")
            sys.exit(1)

        try:
            response = requests.get(self.url, timeout=5)
            response.raise_for_status()
        except requests.exceptions.RequestException as err:
            print(f"Error occurred: {err}")
            sys.exit(1)

        try:
            requirements: list = [
                line.strip()
                for line in response.text.split("\n")
                if line and not line.startswith("#")
            ]
        except Exception as err:
            print(f"Error occurred while parsing the response: {err}")
            sys.exit(1)

        return requirements

    def remove_version(self, dependency: str) -> str:
        # Define the list of operators
        operators: list[str] = [">=", "<=", "==", "<", ">"]

        # Check for each operator in the dependency
        for operator in operators:
            if operator in dependency:
                # Split the dependency on the operator and keep the first part
                # For example, if dependency is "numpy>=1.18.5", dep will be "numpy"
                dep: str = dependency.split(operator)[0]

                return self.remove_inline_comments(dep)

        # If no operator found, return the dependency
        # For example, if dependency is "numpy", it will return "numpy"
        return dependency.strip()

    def remove_inline_comments(self, dependency: str) -> str:
        if "#" in dependency:
            # For example, if dependency is "numpy # numpy is a dependency", dep will be "numpy"
            dep = dependency.split("#")[0]

            return dep.strip()

        # If no inline comment found, return the dependency
        # For example, if dependency is "numpy", it will return "numpy"
        return dependency.strip()

    def install(self, latest: bool = False, reinstall: bool = False) -> None:
        cmd = [sys.executable, "-m", "pip", "install"]

        if reinstall:
            cmd.append("--force-reinstall")

        for dep in self.fetch_requirements():
            dep = self.remove_inline_comments(dep)
            if latest:
                dep: str = self.remove_version(dep)

            cmd.append(dep.strip())

        print("Installing dependencies...")
        try:
            subprocess.check_call(cmd, stdout=sys.stdout)
        except subprocess.CalledProcessError as err:
            print(f"Error occurred while installing dependencies: {err}")
            sys.exit(1)


class Handler:
    def __init__(self):
        self.handlers: dict = {}

    def add_handler(self, name, handler):
        self.handler_check(name, handler)
        self.handlers[name] = handler

    def handler_check(self, name, handler):
        self.check_name(name)
        self.check_callable(handler)
        self.check_existence(name)

    def check_name(self, name):
        if not name:
            raise ValueError("Handler must have a name")

    def check_callable(self, handler):
        if not callable(handler):
            raise ValueError("Handler must be callable")

    def check_existence(self, name):
        if name in self.handlers:
            raise ValueError(f"Handler with name {name} already exists")

    def call_handler(self, name, *args, **kwargs):
        if name not in self.handlers:
            raise ValueError(f"Handler with name {name} does not exist")
        return self.handlers[name](*args, **kwargs)


class Arguments(argparse.ArgumentParser):
    def __init__(self):
        super().__init__(
            prog="control_panel.py",
            description="Control Panel for YOLOv5",
            exit_on_error=True,
            add_help=True,
            usage="%(prog)s [options]",
        )

    def store_true(self, *args, **kwargs):
        self.add_argument(*args, **kwargs, action="store_true")


def dependency_handler(**kwargs):
    dependency = Dependency()
    dependency.install(
        kwargs["latest"] if "latest" in kwargs else False,
        kwargs["reinstall"] if "reinstall" in kwargs else False,
    )


def main():
    argument = Arguments()
    argument.store_true("-c", "--clean", help="Clean the Python cache folder")
    argument.store_true("-i", "--install-deps", help="Install YOLOv5 dependencies")
    argument.store_true(
        "--latest",
        help="Install the latest version of the dependencies. Only works with --install-deps",
    )
    argument.store_true(
        "--reinstall",
        help="Reinstall the dependencies. Only works with --install-deps",
    )
    parsed_arguments = argument.parse_args()

    handler_instance = Handler()
    handler_instance.add_handler("clean", remove_cache)
    handler_instance.add_handler(
        "install_deps",
        partial(
            dependency_handler,
            latest=parsed_arguments.latest,
            reinstall=parsed_arguments.reinstall,
        ),
    )

    for key, value in vars(parsed_arguments).items():
        if isinstance(value, bool):
            if key in handler_instance.handlers and value:
                handler_instance.call_handler(key)


if __name__ == "__main__":
    main()
