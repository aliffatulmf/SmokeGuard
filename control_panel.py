import logging
from cmd.args import CommandArguments

from libs.handler.command_handler import command_handlers
from libs.handler.command_validation import command_validation
from libs.logger import console

HEADER = """
███████ ███    ███  ██████  ██   ██ ███████      ██████  ██    ██  █████  ██████  ██████
██      ████  ████ ██    ██ ██  ██  ██          ██       ██    ██ ██   ██ ██   ██ ██   ██
███████ ██ ████ ██ ██    ██ █████   █████       ██   ███ ██    ██ ███████ ██████  ██   ██
     ██ ██  ██  ██ ██    ██ ██  ██  ██          ██    ██ ██    ██ ██   ██ ██   ██ ██   ██
███████ ██      ██  ██████  ██   ██ ███████      ██████  ████████ ██   ██ ██   ██ ██████
[italic][bold red]Control Panel[/bold red] [underline]based on[/underline] [bold blue]Ultralytics/YOLOv5[/bold blue][/italic]
"""

if __name__ == "__main__":
    console.print(HEADER, style="cyan", justify="center")

    logging.disable()

    cmd_args = CommandArguments().parse()
    cmd_kwargs = vars(cmd_args)

    if bool(command_validation(**cmd_kwargs)):
        command_handlers(**cmd_kwargs)
