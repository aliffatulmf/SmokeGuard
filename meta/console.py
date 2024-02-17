"""
Meta Console
"""

import sys

from rich.console import Console

_console = Console()

def print(*args, **kwargs):
    _console.print(*args, **kwargs)

def fatal(*args, **kwargs):
    _console.print(*args, **kwargs)
    sys.exit(1)
