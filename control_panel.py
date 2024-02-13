import logging
import os
import sys
import textwrap

from rich.logging import RichHandler

MENU = textwrap.dedent("""
Smoker Control Panel

Options:
   run             - Start the program
   clean           - Clean the cache to free up storage
   help, --help    - Show this help message and exit
""")

def setup_hub():
   if not os.path.exists("hub"):
       import shutil

       import git

       print("=" * 10, "CLONE YOLOv5", "=" * 10)

       os.makedirs("hub", 0o777)
       repo_url = "https://github.com/ultralytics/yolov5"
       repo = git.Repo.clone_from(repo_url, "hub")

   if not os.path.exists("utils"):
       shutil.move("hub/utils", "utils")

   if not os.path.exists("models"):
       shutil.move("hub/models", "models")

   if not os.path.exists("export.py"):
       shutil.move("hub/export.py", ".")

def print_menu():
   print(MENU)

def clean_cache():
   from meta.cache import clean_cache_dir
   clean_cache_dir(".")

def start_program():
   from meta.exec import window
   window()

def main():
   setup_hub()

   logging.basicConfig(
       level=logging.NOTSET,
       format="%(message)s",
       datefmt="[%X]",
       handlers=[RichHandler(omit_repeated_times=False)],
   )

   arg = sys.argv[1] if len(sys.argv) > 1 else "help"

   functions = {
       "help": print_menu,
       "clean": clean_cache,
       "run": start_program,
   }

   if arg.lower() in functions:
       functions[arg.lower()]()
   else:
       print_menu()

if __name__ == "__main__":
   main()