import logging
import sys
import textwrap

MENU = textwrap.dedent("""Smoker Control Panel

options:
    run             - start the program
    clean           - clean the cache to free up storage
    help, --help    - show this help message and exit
    """)

def setup_hub():
    import os
    import shutil

    if not os.path.exists("hub"):
        from git import Repo

        os.makedirs("hub", 777)
        repo_url = "https://github.com/ultralytics/yolov5"
        repo = Repo.clone_from(repo_url, "hub")

    if not os.path.exists("utils"):
        shutil.move("hub/utils", "utils")
    
    if not os.path.exists("models"):
        shutil.move("hub/models", "models")
    
    if not os.path.exists("export.py"):
        shutil.move("hub/export.py", ".")
 
if __name__ == "__main__":
    setup_hub()
    from rich.logging import RichHandler

    logging.basicConfig(
        level=logging.NOTSET,
        format="%(message)s",
        datefmt="[%X]", handlers=[RichHandler(omit_repeated_times=False)],
    )

    arg = sys.argv[1] if len(sys.argv) > 1 else "help"

    if arg.lower() in ["help", "--help"]:
        print(MENU)
    elif arg.lower() == "run":
        from meta.exec import window
        window()
    else:
        print(MENU)
