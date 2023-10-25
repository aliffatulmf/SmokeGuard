import os
import shutil

from rich.console import Console

console = Console()


def remove_cache() -> None:
    cache_found = False

    for dirPath, _, _ in os.walk("."):
        if dirPath.endswith("__pycache__"):
            try:
                console.print(
                    f"[bold red][REMOVE][/bold red][italic red] {dirPath}[/italic red]"
                )
                shutil.rmtree(dirPath)
                cache_found = True
            except Exception as e:
                print(f"Error occurred while removing cache: {e}")

    if not cache_found:
        print("No cache found")
