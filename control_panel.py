import logging
import os
import signal
import sys
import textwrap

from pkg.cache import clean_python_cache
from pkg.exec import run
from validator.requirements import check_requirements

HEADER = """
███████ ███    ███  ██████  ██   ██ ███████      ██████  ██    ██  █████  ██████  ██████
██      ████  ████ ██    ██ ██  ██  ██          ██       ██    ██ ██   ██ ██   ██ ██   ██
███████ ██ ████ ██ ██    ██ █████   █████       ██   ███ ██    ██ ███████ ██████  ██   ██
     ██ ██  ██  ██ ██    ██ ██  ██  ██          ██    ██ ██    ██ ██   ██ ██   ██ ██   ██
███████ ██      ██  ██████  ██   ██ ███████      ██████  ████████ ██   ██ ██   ██ ██████
[italic][bold red]Control Panel[/bold red] [underline]based on[/underline] [bold blue]Ultralytics/YOLOv5[/bold blue][/italic]
"""

def main():
    arg = sys.argv[1] if len(sys.argv) > 1 else "help"

    MENU = textwrap.dedent("""
    options:
        run         - start the program
        clean-cache - clean the cache to free up storage
        help        - show this help message and exit
    """)

    OPTIONS = {
        "run": run,
        "clean-cache": clean_python_cache,
        "help": lambda: print(MENU),
        "h": lambda: print(MENU),
        "-h": lambda: print(MENU),
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
    logger.addHandler(RichHandler(show_path=True, markup=True))
    logger.setLevel(logging.INFO)

def signal_handler(sig, frame):
    pid = os.getpid()
    os.kill(pid, signal.SIGTERM)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)

    try:
        check_requirements(["rich"], auto_install=False)
    except Exception as e:
        print(f"The 'rich' package is required but could not be installed. Error: {e}")
        exit(1)

    setup_logging()
    main()