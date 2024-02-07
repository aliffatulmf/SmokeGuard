"""
Meta Parameter

This module contains the layout for the parameter.
"""

from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (QComboBox, QFrame, QGroupBox, QLabel,
                               QPushButton, QSpinBox, QVBoxLayout)

from meta import CONFIG_JSON
from meta.io import ConfigIO

font = QFont()
font.setFamily("JetBrains Mono")
font.setPointSize(10)
font.setWeight(QFont.Weight.Medium)


class Parameter(QFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.setGeometry(20, 40, 300, 700)

        groupbox = QGroupBox()
        groupbox.setFixedHeight(self.geometry().height())
        groupbox.setFixedWidth(self.geometry().width())
        groupbox.setParent(self)

        layout = QVBoxLayout(groupbox)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setSpacing(10)

        self.conf_inp = QSpinBox()
        self.conf_inp.setRange(0, 100)
        self.conf_inp.setValue(int(CONFIG_JSON[ConfigIO.CONFIDENCE] * 100))

        self.iou_inp = QSpinBox()
        self.iou_inp.setRange(0, 100)
        self.iou_inp.setValue(int(CONFIG_JSON[ConfigIO.IOU] * 100))

        self.device_inp = QComboBox()
        self.device_inp.addItems(["CUDA", "CPU"])
        self.device_inp.setCurrentText("CUDA")
        self.device_inp.setDisabled(True)

        self.agnostic_inp = QComboBox()
        self.agnostic_inp.addItems(["Enable", "Disable"])
        self.agnostic_inp.setCurrentText("Enable" if CONFIG_JSON[ConfigIO.AGNOSTIC] else "Disable")

        self.augment_inp = QComboBox()
        self.augment_inp.addItems(["Enable", "Disable"])
        self.augment_inp.setCurrentText("Enable" if CONFIG_JSON[ConfigIO.AUGMENT] else "Disable")

        self.amp_inp = QComboBox()
        self.amp_inp.addItems(["Enable", "Disable"])
        self.amp_inp.setCurrentText("Enable" if CONFIG_JSON[ConfigIO.AMP] else "Disable")

        layout.addWidget(QLabel("Confidence Threshold"))
        layout.addWidget(self.conf_inp)

        layout.addWidget(QLabel("IoU Threshold"))
        layout.addWidget(self.iou_inp)

        layout.addWidget(QLabel("Hardware Acceleration"))
        layout.addWidget(self.device_inp)

        layout.addWidget(QLabel("Agnostic NMS"))
        layout.addWidget(self.agnostic_inp)

        layout.addWidget(QLabel("Augmentation"))
        layout.addWidget(self.augment_inp)

        layout.addWidget(QLabel("Automatic Mixed Precision"))
        layout.addWidget(self.amp_inp)

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_config)
        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self.reset_config)
        layout.addWidget(self.save_button)
        layout.addWidget(self.reset_button)

        self.frames = QLabel("Frames: 0")
        self.frames.setFont(font)
        self.objects = QLabel("Object Detected: 0")
        self.objects.setFont(font)

        self.v_fps = QLabel("0, 0, 0, 0")
        self.v_fps.setFont(font)
        self.v_inference = QLabel("0ms, 0ms, 0ms, 0ms")
        self.v_inference.setFont(font)

        l_fps = QLabel("FPS [Min, Max, Avg]:")
        l_fps.setFont(font)
        l_inf = QLabel("Inference Times [Min, Max, Avg]:")
        l_inf.setFont(font)

        layout.addWidget(self.frames)
        layout.addWidget(self.objects)
        layout.addWidget(l_fps)
        layout.addWidget(self.v_fps)
        layout.addWidget(l_inf)
        layout.addWidget(self.v_inference)

        self.setLayout(layout)

    def save_config(self):
        confidence = self.conf_inp.value() / 100
        iou = self.iou_inp.value() / 100
        agnostic = self.agnostic_inp.currentText() == "Enable"
        augment = self.augment_inp.currentText() == "Enable"
        amp = self.amp_inp.currentText() == "Enable"

        cfg_io = ConfigIO()
        cfg_io.write(ConfigIO.CONFIDENCE, confidence)
        cfg_io.write(ConfigIO.IOU, iou)
        cfg_io.write(ConfigIO.AGNOSTIC, agnostic)
        cfg_io.write(ConfigIO.AUGMENT, augment)
        cfg_io.write(ConfigIO.AMP, amp)

    def reset_config(self):
        conf = int(CONFIG_JSON[ConfigIO.CONFIDENCE] * 100)
        iou = int(CONFIG_JSON[ConfigIO.IOU] * 100)
        agnostic = "Enable" if CONFIG_JSON[ConfigIO.AGNOSTIC] else "Disable"
        augment = "Enable" if CONFIG_JSON[ConfigIO.AUGMENT] else "Disable"
        amp = "Enable" if CONFIG_JSON[ConfigIO.AMP] else "Disable"

        self.conf_inp.setValue(conf)
        self.iou_inp.setValue(iou)
        self.agnostic_inp.setCurrentText(agnostic)
        self.augment_inp.setCurrentText(augment)
        self.amp_inp.setCurrentText(amp)

    @Slot(object)
    def signal_receiver(self, param: dict):
        frames_text = f"Frames: {param['frames']}"
        self.frames.setText(frames_text)
        self.frames.setFont(font)

        objects_text = f"Object Detected: {param['total_object']}"
        self.objects.setText(objects_text)
        self.objects.setFont(font)

        fps_text = f"{int(param['fps']['current'])}, {int(param['fps']['min'])}, {int(param['fps']['max'])}, {int(param['fps']['avg'])}"
        self.v_fps.setText(fps_text)
        self.v_fps.setFont(font)

        inference_text = f"{param['inference']['current']:.2f}ms, {param['inference']['min']:.2f}ms, {param['inference']['max']:.2f}ms, {param['inference']['avg']:.2f}ms"
        self.v_inference.setText(inference_text)
        self.v_inference.setFont(font)
