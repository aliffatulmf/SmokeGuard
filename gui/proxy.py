from PySide6.QtCore import QObject


def better_proxy(source: QObject, target: any):
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
        print(f"Failed to connect source: {source} to target: {target}, due to error: {ex}")
