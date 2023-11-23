import sys

from libs.logger import console


class ArgumentRequired:
    def __init__(self, **kwargs):
        self.arguments = kwargs

    def _args_required(self):
        if self.command_name in self.arguments:
            for link in self.linked:
                value = self.arguments.get(link)

                if value is not None:
                    value = int(value) if value.isdigit() else str(value)

                if (
                    hasattr(self, "ignore")
                    and link in self.ignore.keys()
                    and value in self.ignore.values()
                ):
                    continue

                if not value:
                    raise ValueError(
                        f"the [bold green]--{self.command_name}[/bold green] requires [bold green]--{link}[/bold green] to execute"
                    )

    @classmethod
    def required(cls, command_name: str, linked: list[str], ignore: dict = {}):
        if command_name == "" or command_name is None:
            raise ValueError("command name cannot be empty")
        else:
            cls.command_name = command_name

        if not linked:
            raise ValueError("linked arguments cannot be empty")
        else:
            cls.linked = linked

        if bool(ignore):
            cls.ignore = ignore

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            self._args_required()
        except ValueError as e:
            console.custom("red", "CMD ERROR", str(e))
            sys.exit(1)
