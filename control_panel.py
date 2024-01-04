import logging
import os
import signal
import sys
import textwrap

from meta.exec import cleaner, run
from meta.repo import GitHubRepository
from meta.requirements import check_requirements

HEADER = """
███████ ███    ███  ██████  ██   ██ ███████      ██████  ██    ██  █████  ██████  ██████
██      ████  ████ ██    ██ ██  ██  ██          ██       ██    ██ ██   ██ ██   ██ ██   ██
███████ ██ ████ ██ ██    ██ █████   █████       ██   ███ ██    ██ ███████ ██████  ██   ██
     ██ ██  ██  ██ ██    ██ ██  ██  ██          ██    ██ ██    ██ ██   ██ ██   ██ ██   ██
███████ ██      ██  ██████  ██   ██ ███████      ██████  ████████ ██   ██ ██   ██ ██████
[italic][bold red]Control Panel[/bold red] [underline]based on[/underline] [bold blue]Ultralytics/YOLOv5[/bold blue][/italic]
"""


def main():
    from rich.console import Console
    console = Console()
    
    arg = sys.argv[1] if len(sys.argv) > 1 else "help"

    MENU = textwrap.dedent("""
    [bold yellow]options:[/bold yellow]
        [green]run[/green]         - start the program
        [green]clean[/green]       - clean the cache to free up storage
        [green]help[/green]        - show this help message and exit
    """)

    OPTIONS = {
        "run": run,
        "clean": cleaner,
        "help": lambda: console.print(MENU),
        "h": lambda: console.print(MENU),
        "-h": lambda: console.print(MENU),
    }

    try:
        OPTIONS[arg]()
    except KeyError:
        logging.critical(f"Option '{arg}' is not recognized. Use 'help' to see the available options.")
        exit(1)        

def setup_logging():
    from rich.logging import RichHandler

    logger = logging.getLogger()
    logger.handlers.clear()

    # Check if a RichHandler already exists to avoid adding it multiple times
    if not any(isinstance(handler, RichHandler) for handler in logger.handlers):
        rich_handler = RichHandler(show_path=True, markup=True, show_time=True)
        logger.addHandler(rich_handler)

    logger.setLevel(logging.NOTSET)
    
def signal_handler(sig, frame):
    pid = os.getpid()
    os.kill(pid, signal.SIGTERM)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)

    try:
        check_requirements(["rich", "gitpython"], auto=True)
    except Exception as e:
        print(f"An error occurred while checking requirements: {e}")
        exit(1)
        
    repo = GitHubRepository("ultralytics/yolov5", "hub")
    repo.clone()
    
    setup_logging()
    main()