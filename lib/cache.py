import os
import shutil

from lib.logger import console


def remove_cache(excluded_directory: list[str] = [], verbose: bool = False) -> None:
    cache_found = False
    for root, _, _ in os.walk("."):
        if root.endswith("__pycache__"):
            if not any([ed for ed in excluded_directory if ed in root]):
                cache_found = True

                try:
                    shutil.rmtree(root)
                    console.print(
                        f"[bold red][REMOVE][/bold red][italic red] {os.path.dirname(root)}[/italic red]"
                    )
                except Exception as e:
                    print(f"Error occurred while removing cache: {e}")
            elif verbose:
                console.print(f"[bold cyan][SKIP][/bold cyan] {os.path.dirname(root)}")

    if cache_found:
        console.print("[bold green][SUCCESS][/bold green] Successfully removed cache")
    else:
        console.print("[bold yellow][SKIP][/bold yellow] No cache found")
