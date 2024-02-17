"""
Meta Flag

Simple class to store flags and parse them from the command line
"""

import inspect
import sys
import textwrap

import meta.console as console


class FlagSpace:
    def __repr__(self):
        return f"FlagSpace({', '.join([f'{k}={v}' for k, v in vars(self).items()])})"

    def __str__(self):
        return self.__repr__()

    def handler(self, flag, fn, *args, **kwargs):
        fn_params = inspect.signature(fn).parameters
        
        if hasattr(self, flag):
            if len(fn_params) == 0:
                fn()
            else:
                fn(*args, **kwargs)


class NewFlag:
    def __init__(self, name):
        self.registered_flags = {"help": {"usage": "print this help message"}}
        self.format = ""
        self.format += f"  {name}\n\n"

    def bool(self, flag, usage=None):
        self.registered_flags[flag] = {"type": bool, "usage": usage}

    def _format(self):
        max_length = max(len(f) for f in self.registered_flags) + 10
        _format = "  {flag} {space} {usage}\n"

        for flag, options in self.registered_flags.items():
            space = " " * (max_length - len(flag))
            help_text = textwrap.fill(options["usage"], width=100).replace("\n", "\n" + " " * max_length)

            self.format += _format.format(flag=flag, space=space, usage=help_text)

    def help(self):
        self._format()
        console.print(self.format)
        sys.exit(0)

    def parse_args(self):
        namespace = FlagSpace()

        arg = sys.argv[1] if len(sys.argv) > 1 else None
        if arg is None or arg == "help":
            self.help()

        if arg is not None and arg in self.registered_flags.keys():
            if self.registered_flags[arg]["type"] is bool:
                setattr(namespace, arg, True)
        else:
            console.print(f"[red]Error: [/red]'{arg}' is not a valid flag. Use 'help' to see available flags.")

            sys.exit(1)

        return namespace
