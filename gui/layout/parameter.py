import logging

import torch
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (QComboBox, QFrame, QGroupBox, QLabel,
                               QMessageBox, QPushButton, QSpinBox, QVBoxLayout,
                               QWidget)

from pkg.cfg import ConfigValues

config = ConfigValues()

ENABLE = "Enable"
DISABLE = "Disable"
SWITCH = [ENABLE, DISABLE]

PARAMETERS = {
    "conf": {
        "type": "spinbox",
        "label": "Confidence Threshold",
        "minimum": 1,
        "maximum": 100,
        "value": config.get("conf") * 100,
    },
    "iou": {
        "type": "spinbox",
        "label": "IoU Threshold",
        "minimum": 1,
        "maximum": 100,
        "value": config.get("iou") * 100,
    },
    "hardware_acceleration": {
        "type": "choice",
        "label": "Hardware Acceleration",
        "items": ["CPU", "CUDA"],
        "value": "CUDA" if torch.cuda.is_available() else "CPU",
        "disabled": True,
    },
    "agnostic": {
        "type": "dropdown",
        "label": "Class-Agnostic NMS",
        "items": SWITCH,
        "value": config.get("agnostic"),
    },
    "amp": {
        "type": "dropdown",
        "label": "Automatic Mixed Precision",
        "items": SWITCH,
        "value": config.get("amp"),
    },
}


class SettingsLayout:
    def __init__(self, parent: QWidget = None):
        self.parent = parent

        self.frame = QFrame()
        self.frame.setGeometry(20, 50, 200, 768)
        self.frame.setParent(parent)

        self.param_box = QGroupBox()
        self.param_box.setTitle("Parameters")
        self.param_box.setFixedWidth(190)
        self.param_box.setFixedHeight(400)
        self.param_box.setParent(self.frame)

        self.top_vbox = QVBoxLayout(self.param_box)
        self.top_vbox.setAlignment(Qt.AlignmentFlag.AlignTop)

    def save_values(self):
        values = {}
        for k, v in PARAMETERS.items():
            if v["type"] == "spinbox":
                values[k] = self.__dict__[f"{k}_form"].value()
            elif v["type"] == "dropdown":
                values[k] = self.__dict__[f"{k}_form"].currentText()

        config.update(values)
        if config.save():
            self.show_save_notif()

    @staticmethod
    def show_save_notif():
        message_box = QMessageBox()
        message_box.setWindowIcon(QIcon("assets/icon/icon.png"))
        message_box.setWindowTitle("Save Notification")
        message_box.setText(
            "Your changes have been successfully saved.\nPlease restart the application for the changes to take effect.")
        message_box.setStandardButtons(QMessageBox.Ok)
        message_box.exec()

    def create_action_buttons(self):
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(lambda: self.save_values())

        reset_btn = QPushButton("Reset")
        reset_btn.clicked.connect(lambda: self.reset_values())

        self.param_box.layout().addWidget(save_btn)
        self.param_box.layout().addWidget(reset_btn)

    def reset_values(self):
        for k, v in PARAMETERS.items():
            if v["type"] == "spinbox":
                self.__dict__[f"{k}_form"].setValue(v["value"])
            elif v["type"] == "dropdown":
                self.__dict__[f"{k}_form"].setCurrentText(
                    ENABLE if v["value"] else DISABLE)
            elif v["type"] == "choice":
                self.__dict__[f"{k}_form"].setCurrentText(v["value"])

    def label(self, text):
        label = QLabel(text, self.param_box)
        self.top_vbox.addWidget(label)
        return label

    def generator(self):
        for key, value in PARAMETERS.items():
            try:
                form_creator = getattr(self, value["type"])
                label = self.label(value["label"])
                form = form_creator(value)
                setattr(self, f"{key}_label", label)
                setattr(self, f"{key}_form", form)
            except ValueError as e:
                logging.error(f"Error creating form for parameter {key}: {e}")

    def spinbox(self, value):
        return self._bounded_form(QSpinBox, value["minimum"], value["maximum"], value["value"])

    def dropdown(self, value):
        dropdown = self._choices_form(
            QComboBox, value["items"], value["value"])
        dropdown.setDisabled(value.get("disabled", False))
        return dropdown

    def choice(self, value):
        choice = self._choices_form(QComboBox, value["items"], value["value"])
        choice.setDisabled(value.get("disabled", False))
        return choice

    def _bounded_form(self, form_class, minimum, maximum, value):
        if not minimum <= value <= maximum:
            raise ValueError(
                f"Invalid value: {value}. Must be in range {minimum} to {maximum}.")
        form = form_class(self.param_box)
        form.setRange(minimum, maximum)
        form.setValue(value)
        self.top_vbox.addWidget(form)
        return form

    def _choices_form(self, form_class, items, value):
        if value not in items:
            raise ValueError(
                f"Invalid value: {value}. Must be in items {items}.")
        form = form_class(self.param_box)
        form.addItems(items)
        form.setCurrentText(value)
        self.top_vbox.layout().addWidget(form)
        return form

    def show(self):
        self.generator()
        self.create_action_buttons()
