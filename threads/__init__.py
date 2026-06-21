import logging
import os

from pkg.requirements import check_requirements

REPO_PATH = "cache/yolov5"


def ensure_yolov5_repo():
    if os.path.exists(REPO_PATH):
        return

    logging.info("YOLOv5 repo not found, cloning...")

    if not check_requirements(["gitpython"], True):
        raise RuntimeError("gitpython is required to clone YOLOv5 repo")

    from git import Repo
    Repo.clone_from("https://github.com/ultralytics/yolov5.git", REPO_PATH)
    logging.info("YOLOv5 repo cloned successfully")


ensure_yolov5_repo()
