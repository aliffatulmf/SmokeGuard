import logging
import os

from shutil import copyfile, copytree, ignore_patterns
from git import Repo, RemoteProgress
from tqdm import tqdm


def setup_hub():
    # https://stackoverflow.com/questions/51045540/python-progress-bar-for-git-clone
    class CloneProcess(RemoteProgress):
        def __init__(self):
            super().__init__()
            self.pbar = tqdm(desc="Cloning")
        
        def update(self, op_code, cur_count, max_count, message=""):
            self.pbar.total = max_count
            self.pbar.n = cur_count
            self.pbar.refresh()

    def clone_repo(repo_url, local_path):
        if not os.path.exists(local_path):
            logging.info(f"Cloning {repo_url} to {local_path}")
            Repo.clone_from(repo_url, local_path, progress=CloneProcess())

    def copy(src, dest):
        if not os.path.exists(dest):
            logging.info(f"Moving {src} to {dest}")
            if os.path.isfile(src):
                copyfile(src, dest, follow_symlinks=False)
            elif os.path.isdir(src):
                copytree(src, dest, ignore=ignore_patterns("*.pyc", "*.pyo", "__pycache__"))

    # clone YOLOv5 repository if it doesn't exist
    if not os.path.isdir("hub"):
        clone_repo("https://github.com/ultralytics/yolov5", "hub")

    # copy utils, models, and export.py if they don't exist
    if not os.path.isfile("export.py"):
        copy("hub/export.py", "export.py")

    if not os.path.isdir("utils"):
        copy("hub/utils", "utils")

    if not os.path.isdir("models"):
        copy("hub/models", "models")