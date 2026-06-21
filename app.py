import argparse
import logging
import sys

HEADER = """
███████ ███    ███  ██████  ██   ██ ███████      ██████  ██    ██  █████  ██████  ██████
██      ████  ████ ██    ██ ██  ██  ██          ██       ██    ██ ██   ██ ██   ██ ██   ██
███████ ██ ████ ██ ██    ██ █████   █████       ██   ███ ██    ██ ███████ ██████  ██   ██
     ██ ██  ██  ██ ██    ██ ██  ██  ██          ██    ██ ██    ██ ██   ██ ██   ██ ██   ██
███████ ██      ██  ██████  ██   ██ ███████      ██████  ████████ ██   ██ ██   ██ ██████
[italic][bold red]SmokeGuard[/bold red] [underline]based on[/underline] [bold blue]Ultralytics/YOLOv5[/bold blue][/italic]
"""


def parse_arguments():
    parser = argparse.ArgumentParser(prog="app.py")
    parser.add_argument("--model", type=str, required=True, help="path to model file (.pt or .onnx)")
    parser.add_argument("--source", default="0", help="input source (0=webcam, file, or directory)")
    parser.add_argument("--device", choices=["cpu", "cuda"], default="cuda", help="device for inference")
    parser.add_argument("--output", default="outputs", help="output directory")
    # parser.add_argument("--run", action="store_true", help="start the program")
    # parser.add_argument("--clean", action="store_true", help="clean the cache to free up memory")
    # parser.add_argument("--gpu-ids", nargs="+", type=int, default=None, help="GPU IDs to use")
    # parser.add_argument("--exclude", nargs="+", default=[], help="directories to exclude from cleaning")
    # parser.add_argument("--format", choices=["image", "video"], default="video", help="recording format")
    # parser.add_argument("--install", nargs="+", type=str, default=None, help="dependencies to install")
    # parser.add_argument("--install-required", action="store_true", help="install all required dependencies")
    # parser.add_argument("--reinstall", action="store_true", help="reinstall all dependencies")
    # parser.add_argument("--supported-formats", action="store_true", help="list supported formats")
    # parser.add_argument("--save", action="store_true", help="save output to file")
    return parser.parse_args()


def setup_logging():
    from pkg.requirements import check_requirements, is_package_installed

    if not is_package_installed("rich"):
        try:
            check_requirements(["rich"], auto_install=True)
        except Exception:
            raise Exception("The 'rich' package is required but could not be installed.")

    from rich.logging import RichHandler
    from rich.console import Console

    logger = logging.getLogger()
    logger.handlers.clear()
    logger.addHandler(RichHandler(show_path=True, markup=True))
    logger.setLevel(logging.INFO)

    console = Console()
    console.print(HEADER, style="cyan", justify="center")


def run_gui(**kwargs):
    from PySide6.QtWidgets import QApplication
    from gui.window import Window
    from pkg.checker import check_compatibility
    from pkg.inference import load_model

    check_compatibility()
    app = QApplication(sys.argv)

    # Load model sebelum Window tampil
    model = load_model(
        kwargs["model"],
        device=kwargs["device"],
        verbose=True
    )
    kwargs["model_instance"] = model

    window = Window(**kwargs)
    window.show()
    exit(app.exec())


def run_cli(opt):
    from pkg.exec import Executor

    with Executor(opt) as executor:
        try:
            import funcs
            executor.target(funcs.run_func, True)
            executor.target(funcs.clean_func, False)
            executor.target(funcs.install_func, False)
            executor.target(funcs.supported_formats_func, False)
        except Exception as e:
            logging.error(e)
            exit(1)


if __name__ == "__main__":
    opt = parse_arguments()
    setup_logging()

    kwargs = {
        "model": opt.model,
        "source": opt.source,
        "device": opt.device,
        "output": opt.output
    }

    run_gui(**kwargs)
