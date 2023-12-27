import os

from pkg.requirements import check_requirements

REPO_PATH = "cache/yolov5"

if not os.path.exists(REPO_PATH):
    if check_requirements(["gitpython"], True):
        from git import Repo

    Repo.clone_from("https://github.com/ultralytics/yolov5.git", REPO_PATH)
