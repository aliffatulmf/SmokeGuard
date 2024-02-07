import argparse
import sys

from PySide6.QtWidgets import QApplication

from layout.window import Window


def window():
    """
    A description of the entire function, its parameters, and its return types.
    """
    parser = argparse.ArgumentParser(description="This script allows you to configure the device, model, source, and save and verbose options for running an inference", prog="control_panel.py run")
    parser.add_argument("--half", action="store_true", help="specify whether to use half precision for inference. if specified, half precision is used")
    parser.add_argument("--source", default="0", help="specify the source for inference. the default value is 0")
    parser.add_argument("--models", nargs="+", default=[], help="specify models")
    parser.add_argument("--maxlim", type=int, default=50, help="set the maximum snapshot limit. use 0 for no limit.")
    args = parser.parse_args(sys.argv[2:])

    param = vars(args)
    
    app = QApplication([])
    window = Window(**param)
    window.show()
    app.exec()
