import logging

from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (QComboBox, QFrame, QGroupBox, QLabel,
                               QPushButton, QSpinBox, QVBoxLayout)

from meta import CONFIG_READ
from meta.io import ConfigIO, Font
from meta.signal import ParameterNamespace


class ParametersLayout(QFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent)
        self.setGeometry(20, 40, 300, 650)
        
        self.device = kwargs["device"]
        self.verbose = kwargs["verbose"]

        self.gpbox = QGroupBox()
        self.gpbox.setTitle("Parameters")
        self.gpbox.setFixedWidth(300)
        self.gpbox.setFixedHeight(650)
        self.gpbox.setParent(self)

        self.layout = QVBoxLayout(self.gpbox)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout.setSpacing(8)
        
        # SpinBox untuk confidence dan iou threshold
        self.confidence_spinbox = QSpinBox()
        self.confidence_spinbox.setRange(0, 100)
        self.confidence_spinbox.setValue(int(CONFIG_READ[ConfigIO.CONFIDENCE] * 100))
        
        self.iou_threshold_spinbox = QSpinBox()
        self.iou_threshold_spinbox.setRange(0, 100)
        self.iou_threshold_spinbox.setValue(int(CONFIG_READ[ConfigIO.IOU] * 100))

        # ComboBox untuk hardware acceleration
        self.hardware_acceleration_combobox = QComboBox()
        self.hardware_acceleration_combobox.addItems(["CUDA", "CPU"])
        self.hardware_acceleration_combobox.setCurrentText("CUDA" if self.device == "cuda" else "CPU")
        self.hardware_acceleration_combobox.setDisabled(True)

        # ComboBox untuk agnostic augment dan amp
        self.agnostic_combobox = QComboBox()
        self.agnostic_combobox.addItems(["Enable", "Disable"])
        self.agnostic_combobox.setCurrentText("Enable" if CONFIG_READ[ConfigIO.AGNOSTIC] else "Disable")
        
        self.augment_combobox = QComboBox()
        self.augment_combobox.addItems(["Enable", "Disable"])
        self.augment_combobox.setCurrentText("Enable" if CONFIG_READ[ConfigIO.AUGMENT] else "Disable")
        
        self.amp_combobox = QComboBox()
        self.amp_combobox.addItems(["Enable", "Disable"])
        self.amp_combobox.setCurrentText("Enable" if CONFIG_READ[ConfigIO.AMP] else "Disable")

        # Tambahkan widget ke layout
        self.layout.addWidget(QLabel("Confidence Threshold"))
        self.layout.addWidget(self.confidence_spinbox)

        self.layout.addWidget(QLabel("IoU Threshold"))
        self.layout.addWidget(self.iou_threshold_spinbox)

        self.layout.addWidget(QLabel("Hardware Acceleration"))
        self.layout.addWidget(self.hardware_acceleration_combobox)

        self.layout.addWidget(QLabel("Agnostic NMS"))
        self.layout.addWidget(self.agnostic_combobox)
        
        self.layout.addWidget(QLabel("Augmentation"))
        self.layout.addWidget(self.augment_combobox)

        self.layout.addWidget(QLabel("Automatic Mixed Precision"))
        self.layout.addWidget(self.amp_combobox)

        # Tambahkan tombol save dan reset
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_config)
        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self.reset_config)
        self.layout.addWidget(self.save_button)
        self.layout.addWidget(self.reset_button)
        
        self.font = Font(12, weight=QFont.Weight.Medium)
        self.label_frames = QLabel("Frames: 0")
        self.label_frames.setFont(self.font)
        self.label_objects_detected = QLabel("Object Detected: 0")
        self.label_objects_detected.setFont(self.font)
        self.label_fps_values = QLabel("0, 0, 0, 0")
        self.label_fps_values.setFont(self.font)
        self.label_inference_times = QLabel("0ms, 0ms, 0ms, 0ms")
        self.label_inference_times.setFont(self.font)
        
        self.label_fps = QLabel("FPS [Min, Max, Avg]:")
        self.label_fps.setFont(self.font)
        self.label_inference = QLabel("Inference Times [Min, Max, Avg]:")
        self.label_inference.setFont(self.font)

        self.layout.addWidget(self.label_frames)
        self.layout.addWidget(self.label_objects_detected)
        self.layout.addWidget(self.label_fps)
        self.layout.addWidget(self.label_fps_values)
        self.layout.addWidget(self.label_inference)
        self.layout.addWidget(self.label_inference_times)
        
    def save_config(self):
        if self.verbose:
            logging.info("Saving configuration")
            
        # Declare variables
        confidence_value = self.confidence_spinbox.value() / 100
        iou_value = self.iou_threshold_spinbox.value() / 100
        device_value = "cuda" if self.hardware_acceleration_combobox.currentText() == "CUDA" else "cpu"
        agnostic_value = True if self.agnostic_combobox.currentText() == "Enable" else False
        augment_value = True if self.augment_combobox.currentText() == "Enable" else False
        amp_value = True if self.amp_combobox.currentText() == "Enable" else False

        # Save values
        config_io = ConfigIO()
        config_io.update_config(ConfigIO.CONFIDENCE, confidence_value)
        config_io.update_config(ConfigIO.IOU, iou_value)
        config_io.update_config(ConfigIO.DEVICE, device_value)
        config_io.update_config(ConfigIO.AGNOSTIC, agnostic_value)
        config_io.update_config(ConfigIO.AUGMENT, augment_value)
        config_io.update_config(ConfigIO.AMP, amp_value)

    def reset_config(self):
        if self.verbose:
            logging.info("Resetting configuration")
        # Declare variables
        confidence_value = int(CONFIG_READ[ConfigIO.CONFIDENCE] * 100)
        iou_value = int(CONFIG_READ[ConfigIO.IOU]* 100)
        # device_value = "CUDA" if CONFIG_READ[ConfigIO.DEVICE] == "cuda" else "CPU"
        agnostic_value = "Enable" if CONFIG_READ[ConfigIO.AGNOSTIC] else "Disable"
        augment_value = "Enable" if CONFIG_READ[ConfigIO.AUGMENT] else "Disable"
        amp_value = "Enable" if CONFIG_READ[ConfigIO.AMP] else "Disable"

        # Reset values
        self.confidence_spinbox.setValue(confidence_value)
        self.iou_threshold_spinbox.setValue(iou_value)
        # self.hardware_acceleration_combobox.setCurrentText(device_value)
        self.agnostic_combobox.setCurrentText(agnostic_value)
        self.augment_combobox.setCurrentText(augment_value)
        self.amp_combobox.setCurrentText(amp_value)
    
    @Slot(ParameterNamespace)
    def signal_receiver(self, signal):
        # Declare variables
        frames_value = f"Frames: {signal.frames}"
        objects_detected_value = f"Object Detected: {signal.total_object}"
        fps_values_value = f"{int(signal.fps[0])}, {int(signal.fps[1])}, {int(signal.fps[2])}, {int(signal.fps[3])}"
        inference_times_value = f"{signal.inference[0]:.2f}ms, {signal.inference[1]:.2f}ms, {signal.inference[2]:.2f}ms, {signal.inference[3]:.2f}ms"

        # Update labels
        self.label_frames.setText(frames_value)
        self.label_frames.setFont(self.font)
        
        self.label_objects_detected.setText(objects_detected_value)
        self.label_objects_detected.setFont(self.font)

        self.label_fps_values.setText(fps_values_value)
        self.label_fps_values.setFont(self.font)

        self.label_inference_times.setText(inference_times_value)
        self.label_inference_times.setFont(self.font)