from typing import Callable

from PySide6.QtCore import SignalInstance


def better_proxy(source: SignalInstance, target: Callable):
    """
    +--------+       +--------+
    | thread | ----> | layout | ----
    +--------+       +--------+    |
        |                          |
        v                          v
    +----------+             +-------------+
    | new proxy | --direct--> | main window |
    +----------+             +-------------+
        ^                          ^
        |                          |
    +----------+                   |
    | snapshot | -------------------
    +----------+
    """
    try:
        source.connect(target)
    except Exception as ex:
        print(
            f"Failed to connect source: {source} to target: {target}, due to error: {ex}"
        )
