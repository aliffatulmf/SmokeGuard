import os

from git import Repo

REPO_PATH = "cache/yolov5"

if not os.path.exists(REPO_PATH):
    Repo.clone_from("https://github.com/ultralytics/yolov5.git", REPO_PATH)
