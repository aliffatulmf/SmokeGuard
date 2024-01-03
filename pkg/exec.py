import sys

from PySide6.QtWidgets import QApplication

from gui.window import Window


def run():
    def parseargs():
        import argparse

        parser = argparse.ArgumentParser(description="This script allows you to configure the device, model, source, and save and verbose options for running an inference.", prog="control_panel.py run")
        parser.add_argument("--device", choices=["cpu", "cuda"], default="cuda", help="specify the device to be used for inference. options are 'cpu' or 'cuda'. by default, 'cuda' is used. if 'cuda' is unavailable, 'cpu' is used.")
        parser.add_argument("--single", action="store_true", help="specify whether to use a single model for inference. if specified, a single model is used.")
        parser.add_argument("--source", default="0", help="specify the source for inference. the default value is 0.")
        parser.add_argument("--verbose", action="store_true", help="specify whether to display verbose output. if specified, verbose output is displayed.")
        return parser

    parser = parseargs()
    args = parser.parse_args(sys.argv[2:])

    app = QApplication([])
    window = Window(**vars(args))
    window.showMaximized()
    app.exec()
