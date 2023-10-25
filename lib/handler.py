import sys

from rich.console import Console

from .dependency import Module

console = Console()


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


def dependency_handler(**kwargs):
    module = Module()

    if "name" not in kwargs or kwargs["name"] == "":
        console.print("[bold red][ERROR] --name is required[/bold red]")
        sys.exit(1)

    module.install_required(kwargs["name"], kwargs["reinstall"])
