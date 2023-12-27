
import logging

from rich.console import Console
from rich.table import Table

from pkg.cache import PyCacheManager
from pkg.requirements import check_requirements

console = Console()


def clean_func(opt):
    try:
        pycm = PyCacheManager(opt.exclude)
        pycm.clean()
    except Exception as e:
        logging.critical(e)


def install_func(opt):
    try:
        check_requirements(opt.install, auto_install=True)
        logging.log("All packages are installed.")
    except Exception as e:
        logging.critical(e)


def run_func(opt):
    from app import run
    try:
        run(source=opt.source, model=opt.model,
            device=opt.device, format=opt.format)
    except Exception as e:
        logging.critical(f"RUN {e}")


def supported_formats_func(opt):
    SUPPORTED_FORMATS = [
        [".pt", "PyTorch"],
    ]

    table = Table(title="Supported Formats", show_header=True,
                  header_style="bold magenta")
    table.add_column("Format", justify="center", style="cyan")
    table.add_column("Description", justify="center", style="cyan")

    for format in SUPPORTED_FORMATS:
        table.add_row(format[0], format[1])

    console.print(table, justify="center")
