"""
Meta Cache

This module contains the cache utility.
"""

import os
from shutil import rmtree

import meta.console as console


def clean_cache_dir(root):
    n = 0
    for path, _, _ in os.walk(root):
        if not path.endswith("__pycache__"):
            continue

        try:
            rmtree(path)
            n += 1
        except Exception as e:
            console.fatal(f"Failed to remove {path} directory: {e}")
    return n
