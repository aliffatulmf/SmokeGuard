import argparse
import os
import shutil
import subprocess
import sys
import requests
import socket

FMT_OPT = {
    "formatter": "yapf",
    "style": "google",
    "inplace": True,
}

def remove_cache() -> None:
    for dirPath, _, _ in os.walk("."):
        try:
            if dirPath.endswith("__pycache__"):
                print(f"Removing {dirPath}")
                shutil.rmtree(dirPath)
        except Exception as e:
            print(f"Failed to remove {dirPath} due to {str(e)}")

def is_online() -> bool:
    try:
        socket.create_connection(("1.1.1.1", 443), 2)
        return True
    except OSError as err:
        print(f"OS Error: {err}")
    return False

def clean_text(text: str) -> str:
    return text.split("#")[0].strip()

def fetch_requirements() -> list:
    if not is_online():
        print("You are offline. Please connect to the internet first.")
        sys.exit(1)

    url: str = "https://raw.githubusercontent.com/ultralytics/yolov5/master/requirements.txt"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except requests.exceptions.RequestException as err:
        print(f"Error occurred: {err}")
        sys.exit(1)

    try:
        requirements: list = [line.strip() for line in response.text.split("\n") if line and not line.startswith("#")]
    except Exception as err:
        print(f"Error occurred while parsing the response: {err}")
        sys.exit(1)

    return requirements

def install_dependencies() -> None:
    deps: list = fetch_requirements()
    for dep in deps:
        print("Installing", dep)
        subprocess.run([sys.executable, "-m", "pip", "install", dep])

def format_code(path: str) -> None:
    print("Formatting", path)
    subprocess.run(["yapf", "-i", path])

def main():
    parser = argparse.ArgumentParser(description="Control Panel for YOLOv5")
    parser.add_argument("-c", "--clear-cache", action="store_true", help="Clean the Python cache folder")
    parser.add_argument("-i", "--install-deps", action="store_true", help="Install YOLOv5 dependencies")
    fmt_group = parser.add_argument_group(title="format arguments")
    fmt_group.add_argument("-f", "--fmt-input", type=str, help="Input file or directory to format")
    args = parser.parse_args()

    handlers = {
        "clear_cache": remove_cache,
        "install_deps": install_dependencies,
        "fmt_input": lambda: format_code(args.fmt_input),
    }

    for key, value in vars(args).items():
        if value:
            handlers[key]()

if __name__ == "__main__":
    main()