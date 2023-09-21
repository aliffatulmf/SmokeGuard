from PySide6.QtCore import QObject


def proxy(source: QObject, target: any):
        """
        +--------+       +--------+
        | thread | ----> | layout | ----
        +--------+       +--------+    | 
            |                          |
            v                          v
        +-------+                +-------------+
        | proxy | --short way--> | main window |
        +-------+                +-------------+
            ^                          ^
            |                          |
        +----------+                   |
        | snapshot | -------------------
        +----------+
        """
        source.connect(target)
