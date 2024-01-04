import logging
import os
import shutil


def delete_cache(exclude=[], verbose=False):
    exclude.extend([".git", ".vscode"])
    extensions = ['__pycache__', '.pyc', '.pyd', '.pyo']
    for root, dirs, files in os.walk(os.getcwd()):
        for name in files+dirs:
            if any(name.endswith(ext) for ext in extensions) and name not in exclude:
                path = os.path.join(root, name)
                is_dir = os.path.isdir(path)
                try:
                    shutil.rmtree(path) if is_dir else os.remove(path)
                    if verbose: logging.info(f'[red]Deleted[/red] {path}')
                except Exception as e:
                    logging.error(f'Failed to delete {"directory" if is_dir else "file"} {path}. Error: {e}')
    logging.info("Cache deleted successfully")