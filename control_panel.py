import argparse
import logging

from pkg.exec import Executor
from pkg.requirements import check_requirements, is_package_installed

HEADER = """
███████ ███    ███  ██████  ██   ██ ███████      ██████  ██    ██  █████  ██████  ██████
██      ████  ████ ██    ██ ██  ██  ██          ██       ██    ██ ██   ██ ██   ██ ██   ██
███████ ██ ████ ██ ██    ██ █████   █████       ██   ███ ██    ██ ███████ ██████  ██   ██
     ██ ██  ██  ██ ██    ██ ██  ██  ██          ██    ██ ██    ██ ██   ██ ██   ██ ██   ██
███████ ██      ██  ██████  ██   ██ ███████      ██████  ████████ ██   ██ ██   ██ ██████
[italic][bold red]Control Panel[/bold red] [underline]based on[/underline] [bold blue]Ultralytics/YOLOv5[/bold blue][/italic]
"""


def parse_arguments():
    parser = argparse.ArgumentParser(prog="control_panel.py")
    parser.add_argument("--run", action="store_true", help="start the program")
    parser.add_argument("--clean", action="store_true", help="clean the cache to free up memory")
    parser.add_argument("--device", choices=["cpu", "cuda"], default="cuda", help="choose the device to use for inference. Options are 'cpu' and 'cuda'")
    parser.add_argument("--gpu-ids", nargs="+", type=int, default=None, help="specify the GPU IDs to use for inference")
    parser.add_argument("--exclude", nargs="+", default=[], help="specify directories to exclude from the cache cleaning")
    parser.add_argument("--format", choices=["image", "video"], default="video", help="choose the format to use for recording. Options are 'image' and 'video'")
    parser.add_argument("--install", nargs="+", type=str, default=None, help="specify dependencies to install")
    parser.add_argument("--install-required", action="store_true", help="install all required dependencies")
    parser.add_argument("--model", type=str, default=None, help="specify the path to the model file")
    parser.add_argument("--reinstall", action="store_true", help="reinstall all required dependencies")
    parser.add_argument("--source", default="0", help="specify the source to use for inference")
    parser.add_argument("--supported-formats", action="store_true", help="list all supported formats")
    parser.add_argument("--save", action="store_true", help="save the output to a file")
    parser.add_argument("--output", default="outputs", help="specify the output directory")
    return parser.parse_args()


def main():
    opt = parse_arguments()
    
    with Executor(opt) as e:
        try:
            import funcs
            e.target(funcs.run_func, opt.run)
            e.target(funcs.clean_func, opt.clean)
            e.target(funcs.install_func, opt.install_required)
            e.target(funcs.supported_formats_func, opt.supported_formats)
        except Exception as e:
            logging.error(e)
            exit(1)


if __name__ == "__main__":
    if not is_package_installed("rich"):
        try:
            check_requirements(["rich"], auto_install=True)
        except Exception as e:
            raise Exception("The 'rich' package is required but could not be installed.")

    from rich.logging import RichHandler
    logger = logging.getLogger()
    logger.handlers.clear()
    logger.addHandler(RichHandler(show_path=True, markup=True))
    logger.setLevel(logging.INFO)

    from rich.console import Console
    console = Console()
    console.print(HEADER, style="cyan", justify="center")

    main()
