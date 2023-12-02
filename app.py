import sys

from PySide6.QtWidgets import QApplication

from gui.window import Window
from libs.logger import console
from validation import *


def prerun_check():
    """
    Performs pre-run checks to ensure system compatibility and correct Python version.

    This function checks if the system is compatible with the requirements and if the Python version is 3.9.0 or higher.
    If any of these checks fail, the function raises an exception and the program terminates.

    Raises:
        Exception: If the system is not compatible or the Python version is not 3.9.0 or higher.
    """
    try:
        console.info("checking system compatibility...")
        check_system_compat()

        console.info("checking python version...")
        check_python_version

    except Exception as e:
        console.fatal(e)


def run(**kwargs):
    prerun_check()

    kwargs["source"] = check_source(kwargs.get("source"))

    app = QApplication(sys.argv)
    window = Window(**kwargs)
    window.show()
    sys.exit(app.exec())
