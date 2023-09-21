import argparse
import os
import shutil
import subprocess
import sys

import requests


def clean_cache():
    for dirPath, _, _ in os.walk("."):
        if dirPath.endswith("__pycache__"):
            print(f"Removing {dirPath}")
            shutil.rmtree(dirPath)


def check_online():
    import socket

    try:
        socket.create_connection(("1.1.1.1", 443), 5)
        return True
    except OSError:
        pass

    return False


def sanitize_text(text):
    return text.split("#")[0].strip()


def get_requirements():
    if not check_online():
        print("You are offline. Please connect to the internet first.")
        sys.exit(1)

    url = "https://raw.githubusercontent.com/ultralytics/yolov5/master/requirements.txt"

    response = requests.get(url)

    requirements = []
    for line in response.text.split("\n"):
        line = line.strip()
        if line and not line.startswith("#"):
            requirements.append(line)

    return requirements


def install_dependency():
    deps = get_requirements()
    for dep in deps:
        print("Installing", dep)
        subprocess.run([sys.executable, "-m", "pip", "install", dep])


FMT_OPT = {
    "formatter": "yapf",
    "style": "google",
    "inplace": True,
}


def formatter(path: str):
    print("Formatting", path)
    subprocess.run(["yapf", "-i", path])


def main():
    parser = argparse.ArgumentParser(description="Control Panel for YOLOv5")
    parser.add_argument("-cc", "--clean-cache", action="store_true", help="Clean the cache folder")
    parser.add_argument("--install-dependency", action="store_true", help="Install dependencies")

    fmt_group = parser.add_argument_group(title="format arguments")
    fmt_group.add_argument("-fi", "--fmt-input", type=str, help="Input file or directory")

    args = parser.parse_args()

    handlers = {
        "clean_cache": clean_cache,
        "install_dependency": install_dependency,
        "fmt_input": lambda: formatter(args.fmt_input),
    }

    for key, value in vars(args).items():
        if value:
            if isinstance(handlers[key], list):
                for handler in handlers[key]:
                    handler()
            else:
                handlers[key]()


if __name__ == "__main__":
    main()
