
import logging
import sys

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
    from PySide6.QtWidgets import QApplication

    from gui.window import Window

    app = QApplication(sys.argv)
    window = Window(opt)
    window.show()
    sys.exit(app.exec())