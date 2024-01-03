import logging
import pathlib
import shutil


def clean_python_cache(exclude=None):
    exclude = exclude or []
    root_dir = pathlib.Path(".")

    for pycache_dir in root_dir.rglob("*"):
        if pycache_dir.is_dir() and pycache_dir.name not in exclude:
            try:
                if pycache_dir.name == "__pycache__" and any(child.suffix in {'.pyc', '.pyo', '.pyd'} for child in pycache_dir.iterdir()):
                    shutil.rmtree(pycache_dir)
                    logging.info(f"Removed {pycache_dir}")
                else:
                    logging.warning(f"{pycache_dir} is not a valid Python cache directory.")
            except OSError as e:
                logging.error(f"Error: {e.filename} - {e.strerror}.")