import os
import shutil

from libs.logger import console


class CacheError(Exception):
    pass


def is_excluded(root: str, excluded_directory: list[str]):
    return any(exclude for exclude in excluded_directory if exclude in root)


def remove_cache(excluded_directory: list[str] = [], verbose: bool = False) -> None:
    cache_found = False
    print(excluded_directory)
    for root, _, _ in os.walk("."):
        dirname = os.path.dirname(root)
        success_message = (
            f"[bold red][REMOVE][/bold red][italic red] {dirname}[/italic red]"
        )
        skip_message = f"[bold cyan][SKIP][/bold cyan] {dirname}"

        if root.endswith("__pycache__"):
            cache_found = True

            if not is_excluded(root, excluded_directory):
                try:
                    shutil.rmtree(root)
                except Exception as e:
                    raise CacheError(f"Error occurred while removing cache: {e}")
                console.print(success_message)
            else:
                console.print(skip_message)

    if cache_found:
        console.print("[bold green][SUCCESS][/bold green] Successfully removed cache")
    else:
        console.print("[bold yellow][SKIP][/bold yellow] No cache found")
