"""
Meta Cache

This module contains the cache utility.
"""

import os
import pathlib
import shutil


def remove_cache_dir(path):
    path = str(pathlib.Path(path))
    
    if not path.endswith("__pycache__"):
        raise ValueError("path must __pycache__")
    
    try:
        shutil.rmtree(path) 
        return True
    except:
        return False


def clean_cache_dir(root):
    for dir, name, filename in os.walk(root):
        if "__pycache__" in dir and os.path.isdir(dir):
            if remove_cache_dir(dir):
                print(f"remove cache dir: {dir}")
            else:
                print(f"failed to remove cache dir: {dir}")
                