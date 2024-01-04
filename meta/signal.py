from PySide6.QtCore import QObject, Signal, Slot
from PySide6.QtGui import QPixmap

from .namespaces import ParameterNamespace, SnapshotNamespace


class SignalEmitter(QObject):
    camera_signal = Signal(QPixmap)
    snapshot_signal = Signal(SnapshotNamespace)
    parameter_signal = Signal(ParameterNamespace)
    eod_signal = Signal(bool)

    def __init__(self):
        super().__init__()

    def emit_camera_signal(self, pixmap):
        self.camera_signal.emit(pixmap)
    
    def connect_camera_signal(self, func):
        self.camera_signal.connect(func)

    def emit_snapshot_signal(self, ns):
        self.snapshot_signal.emit(ns)
        
    def connect_snapshot_signal(self, func):
        self.snapshot_signal.connect(func)

    def emit_parameter_signal(self, parameter_namespace):
        self.parameter_signal.emit(parameter_namespace)
        
    def connect_parameter_signal(self, func):
        self.parameter_signal.connect(func)

    def emit_end_of_detection_signal(self, end_of_detection):
        self.eod_signal.emit(end_of_detection)


class SignalReceiver(QObject):
    def __init__(self, emitter: SignalEmitter):
        super().__init__()
        self.emitter = emitter

    def connect_signals(self):
        self.emitter.camera_signal.connect(self.on_camera_signal)
        self.emitter.snapshot_signal.connect(self.on_snapshot_signal)
        self.emitter.parameter_signal.connect(self.on_parameter_signal)
        self.emitter.eod_signal.connect(self.on_end_of_detection_signal)

    @Slot()
    def on_camera_signal(self, func, *args, **kwargs):
        self._execute_func(self.emitter.camera_signal, func, *args, **kwargs)

    @Slot()
    def on_snapshot_signal(self, func, *args, **kwargs):
        self._execute_func(self.emitter.snapshot_signal, func, *args, **kwargs)

    @Slot()
    def on_parameter_signal(self, func, *args, **kwargs):
        self._execute_func(self.emitter.parameter_signal, func, *args, **kwargs)

    @Slot()
    def on_end_of_detection_signal(self, func, *args, **kwargs):
        self._execute_func(self.emitter.eod_signal, func, *args, **kwargs)

    def _execute_func(self, signal, func, *args, **kwargs):
        if callable(func):
            signal.connect(func, *args, **kwargs)
