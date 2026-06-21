import logging
import pathlib
import shutil


class PyCacheManager:
    """
    Class for managing Python cache.
    """

    def __init__(self, exclude=None):
        """
        Initialize PyCacheManager with a list of directories to exclude from cleaning.

        Args:
            exclude (list, optional): List of directories to exclude from cleaning. Defaults to None.
        """
        self.exclude = exclude or []
        self.root_dir = pathlib.Path(".")

    def clean(self):
        """
        Clean Python cache.
        """
        for pycache_dir in self.root_dir.rglob("__pycache__"):
            if pycache_dir.name not in self.exclude:
                try:
                    shutil.rmtree(pycache_dir)
                    logging.info(f"Removed {pycache_dir}")
                except OSError as e:
                    logging.error(f"Error: {e.filename} - {e.strerror}")
                    raise
