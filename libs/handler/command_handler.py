import sys

from app import run
from libs.cache import CacheError, remove_cache
from libs.logger import console

from .supported_format import show_supported_formats


def command_handlers(**kwargs):
    clean_arg = kwargs.get("clean", False)
    if clean_arg:
        try:
            exclude = kwargs.get("exclude", [])
            remove_cache(exclude)
        except CacheError as e:
            console.fatal(str(e))
        sys.exit(0)
    if kwargs.get("supported_formats", False):
        show_supported_formats()
        sys.exit(0)

    run_arg = kwargs.get("run", False)
    if run_arg:
        run(**kwargs)
