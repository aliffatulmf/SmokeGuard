import os
import sys

import meta.console as console

from meta.flags import NewFlag
from meta.logger import beauty_logger
from meta.git import setup_hub


def run():
    from argparse import ArgumentParser

    parser = ArgumentParser(prog="control_panel.py run")
    parser.add_argument("--half", action="store_true", help="specify whether to use half precision for inference. if specified, half precision is used")
    parser.add_argument("--source", default="0", help="specify the source for inference. the default value is 0")
    parser.add_argument("--weights", nargs="+", default=[], help="specify weights")
    parser.add_argument("--maxlim", type=int, default=50, help="set the maximum snapshot limit. use 0 for no limit.")
    args = parser.parse_args(sys.argv[2:])

    # if source is not digit and source is not a file, then throw error
    if not args.source.isdigit() and not os.path.isfile(args.source):
        console.print(f"[red]Error: [/red]{args.source} is not available. Please make sure the specified source available.")

    # if weights is not empty and model is not a file, then throw error
    if len(args.weights) != 0:
        for model in args.weights:
            if not os.path.isfile(model):
                console.fatal(f"[red]Error: [/red]{model} is not found. Please make sure the specified file exists.")
    else:
        console.fatal("[red]Error: [/red]No weights found. Please make sure the 'weights' list is not empty.")

    kwargs = vars(args)

    # open main window below
    from layout.window import main_window_exec
    main_window_exec(kwargs)


def check_system_requirements():
    import platform

    if platform.system() != "Windows":
        console.print("[red]Error: [/red]This program is only supported on Windows.")
        sys.exit(1)

    if sys.maxsize < 2**32:
        console.print("[red]Error: [/red]This program is only supported on 64-bit Windows.")
        sys.exit(1)


def setup(setup_only=False):
    setup_hub()
    console.print("Setup complete.")

    if setup_only:
        sys.exit(0)


def reset():
    from shutil import rmtree
    from subprocess import check_call, CalledProcessError

    try:
        os.remove("export.py")
    except FileNotFoundError:
        pass
    except OSError as e:
        console.fatal(f"Failed to remove export.py: {e}")

    if os.path.exists("hub"):
        try:
            # cannot use rmtree because it will throw PermissionError
            check_call(["cmd.exe", "/c", "RMDIR", "/S", "/Q", "hub"], shell=True)
        except CalledProcessError as e:
            console.fatal(e)

    rmtree("utils", ignore_errors=True)
    rmtree("models", ignore_errors=True)

    console.print("Reset complete.")


def cache():
    from meta.cache import clean_cache_dir

    if clean_cache_dir(os.getcwd()):
        console.print("Cache cleaned successfully.")


def main():
    check_system_requirements()

    flag = NewFlag(name="Control Panel")
    flag.bool("run", "start the program")
    flag.bool("clean", "clean the cache")
    flag.bool("setup", "setup the program")
    flag.bool("reset", "reset the program")

    args = flag.parse_args()
    args.handler("run", run)
    args.handler("clean", cache)
    args.handler("setup", setup, True)
    args.handler("reset", reset)


if __name__ == "__main__":
    beauty_logger()
    main()
