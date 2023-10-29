from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QFrame,
    QGroupBox,
    QLabel,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from config.parameter import ConfigManager
from gui.layout.camera import CameraLayout

ENABLE = "Enable"
DISABLE = "Disable"
SWITCH = [ENABLE, DISABLE]

_local_config = ConfigManager()

PARAMETERS = {
    "confidence_threshold": {
        "type": "spinbox",
        "label": "Confidence Threshold",
        "minimum": 1,
        "maximum": 100,
        "value": _local_config.get("confidence_threshold"),
    },
    "iou_threshold": {
        "type": "spinbox",
        "label": "Overlap Threshold",
        "minimum": 1,
        "maximum": 100,
        "value": _local_config.get("iou_threshold"),
    },
    "hardware_acceleration": {
        "type": "dropdown",
        "label": "Hardware Acceleration",
        "items": ["Automatic"],
        "value": _local_config.get("device"),
        "disabled": True,
    },
    "use_agnostic_nms": {
        "type": "dropdown",
        "label": "Class-Agnostic NMS",
        "items": SWITCH,
        "value": _local_config.get("use_agnostic_nms"),
    },
    "enable_augmentation": {
        "type": "dropdown",
        "label": "Data Augmentation",
        "items": SWITCH,
        "value": _local_config.get("enable_augmentation"),
    },
}


class ParameterLayout:
    def __init__(self, parent: QWidget = None):
        self.parent = parent
        self.camera_layout = None

        self.frame = QFrame()
        self.frame.setGeometry(20, 50, 200, 768)
        self.frame.setParent(parent)

        self.top_groupbox = QGroupBox()
        self.top_groupbox.setTitle("Parameters")
        self.top_groupbox.setFixedWidth(190)
        self.top_groupbox.setFixedHeight(400)
        self.top_groupbox.setParent(self.frame)

        self.top_vbox = QVBoxLayout(self.top_groupbox)
        self.top_vbox.setAlignment(Qt.AlignmentFlag.AlignTop)

    def set_thread(self, layout: CameraLayout = None):
        self.camera_layout = layout

    def _saveValue(self):
        for key, value in PARAMETERS.items():
            if "disabled" not in value:
                if value["type"] == "spinbox":
                    _local_config.set(key, self.__dict__[f"{key}_form"].value())
                elif value["type"] == "dropdown":
                    _local_config.set(
                        key, self.__dict__[f"{key}_form"].currentText() == ENABLE
                    )

        _local_config.save()

        message_box = QMessageBox()
        message_box.setIcon(QMessageBox.Icon.Information)
        message_box.setWindowTitle("Notification")
        message_box.setText("Application will quit to apply changes.")
        message_box.exec()

        self.parent.close()

    def actionButton(self):
        save_btn = QPushButton()
        save_btn.setText("Save")
        save_btn.clicked.connect(lambda: self._saveValue())

        reset_btn = QPushButton()
        reset_btn.setText("Reset")

        # def restart_thread():
        #     self.camera_layout.stop_without_exit()
        #     self.camera_layout.start()

        # restart_btn = QPushButton()
        # restart_btn.setText("Restart")
        # restart_btn.clicked.connect(lambda: restart_thread())

        self.top_vbox.addWidget(save_btn)
        self.top_vbox.addWidget(reset_btn)
        # self.top_vbox.addWidget(restart_btn)

    def show(self):
        self.generator()
        self.actionButton()

    def generator(self):
        for key, value in PARAMETERS.items():
            if value["type"] == "spinbox":
                label = self.label(value["label"])
                form = self.spinbox(value["minimum"], value["maximum"], value["value"])

                setattr(self, f"{key}_label", label)
                setattr(self, f"{key}_form", form)
            elif value["type"] == "dropdown":
                label = self.label(value["label"])
                form = self.dropdown(value["items"], value["value"])
                form.setDisabled(value.get("disabled", False))

                setattr(self, f"{key}_label", label)
                setattr(self, f"{key}_form", form)

    def button(self, text: str) -> QPushButton:
        btn = QPushButton(self.top_groupbox)
        btn.setText(text)
        self.top_vbox.addWidget(btn)
        return btn

    def values(self):
        values = {}
        for key, value in PARAMETERS.items():
            if value["type"] == "spinbox":
                values[key] = self.__dict__[f"{key}_form"].value()
            elif value["type"] == "dropdown":
                values[key] = self.__dict__[f"{key}_form"].currentText()
        return values

    def label(self, text: str) -> QLabel:
        label = QLabel()
        label.setText(text)

        self.top_vbox.addWidget(label)
        return label

    def spinbox(self, minimum: int, maximum: int, value: int) -> QSpinBox:
        spinbox = QSpinBox(self.top_groupbox)
        spinbox.setRange(minimum, maximum)
        spinbox.setValue(value)

        self.top_vbox.addWidget(spinbox)
        return spinbox

    def dropdown(self, items: list, value: bool) -> QComboBox:
        dropdown = QComboBox(self.top_groupbox)
        dropdown.addItems(items)
        dropdown.setCurrentText(ENABLE if value else DISABLE)

        self.top_vbox.layout().addWidget(dropdown)
        return dropdown
