import logging

import torch
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (QComboBox, QFrame, QGroupBox, QHBoxLayout,
                               QLabel, QMessageBox, QPushButton, QSpinBox,
                               QVBoxLayout, QWidget)

from pkg.cfg import ConfigValues

config = ConfigValues()

ENABLE = "True"
DISABLE = "False"
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
        "value": ENABLE if config.get("agnostic") else DISABLE,
    },
    "amp": {
        "type": "dropdown",
        "label": "Automatic Mixed Precision",
        "items": SWITCH,
        "value": ENABLE if config.get("amp") else DISABLE,
    },
}

STYLE_SHEET = """
QFrame {
    background-color: #f5f5f5;
    border: 1px solid #ddd;
    border-radius: 4px;
}
QGroupBox {
    background-color: #ffffff;
    border: 1px solid #ccc;
    border-radius: 4px;
    margin-top: 10px;
    padding-top: 15px;
    font-weight: bold;
    color: #000000;
}
QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 5px;
}
QLabel {
    color: #000000;
    font-size: 11px;
}
QSpinBox, QComboBox {
    background-color: #ffffff;
    border: 1px solid #ccc;
    border-radius: 3px;
    padding: 4px 8px;
    color: #000000;
    min-height: 20px;
}
QComboBox::drop-down {
    border: none;
}
QComboBox::downarrow {
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 6px solid #000000;
    margin-right: 8px;
}
QComboBox QAbstractItemView {
    background-color: #ffffff;
    color: #000000;
    selection-background-color: #4a90d9;
    selection-color: #ffffff;
    border: 1px solid #ccc;
}
QSpinBox:focus, QComboBox:focus {
    border: 1px solid #4a90d9;
}
QPushButton {
    background-color: #e8e8e8;
    border: 1px solid #ccc;
    border-radius: 3px;
    padding: 6px 12px;
    color: #000000;
    font-weight: bold;
    min-height: 20px;
}
QPushButton:hover {
    background-color: #d0d0d0;
}
QPushButton:pressed {
    background-color: #b8b8b8;
}
"""


class SettingsLayout:
    WIDTH = 220
    HEIGHT = 580
    X = 15
    Y = 45
    MARGIN = 10
    SPACING = 12

    def __init__(self, parent: QWidget = None):
        self.parent = parent
        self.styles = STYLE_SHEET

        self.frame = QFrame()
        self.frame.setGeometry(self.X, self.Y, self.WIDTH, self.HEIGHT)
        self.frame.setParent(parent)
        self.frame.setStyleSheet(self.styles)

        self.param_box = QGroupBox("Parameters")
        self.param_box.setFixedWidth(self.WIDTH - 20)
        self.param_box.setFixedHeight(self.HEIGHT - 20)
        self.param_box.setParent(self.frame)
        self.param_box.move(10, 10)

        self.main_layout = QVBoxLayout(self.param_box)
        self.main_layout.setContentsMargins(self.MARGIN, self.MARGIN, self.MARGIN, self.MARGIN)
        self.main_layout.setSpacing(self.SPACING)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

    def save_values(self):
        values = {}
        for k, v in PARAMETERS.items():
            if v["type"] == "spinbox":
                values[k] = self.__dict__[f"{k}_form"].value()
            elif v["type"] == "dropdown":
                text = self.__dict__[f"{k}_form"].currentText()
                values[k] = text == ENABLE

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
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(8)

        save_btn = QPushButton("Save")
        save_btn.clicked.connect(lambda: self.save_values())

        reset_btn = QPushButton("Reset")
        reset_btn.clicked.connect(lambda: self.reset_values())

        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(reset_btn)

        self.main_layout.addStretch()
        self.main_layout.addLayout(btn_layout)

    def reset_values(self):
        for k, v in PARAMETERS.items():
            if v["type"] == "spinbox":
                self.__dict__[f"{k}_form"].setValue(v["value"])
            elif v["type"] == "dropdown":
                self.__dict__[f"{k}_form"].setCurrentText(
                    ENABLE if v["value"] == ENABLE else DISABLE)
            elif v["type"] == "choice":
                self.__dict__[f"{k}_form"].setCurrentText(v["value"])

    def create_field(self, label_text, widget):
        field_layout = QVBoxLayout()
        field_layout.setSpacing(4)

        label = QLabel(label_text)
        field_layout.addWidget(label)
        field_layout.addWidget(widget)

        return field_layout

    def generator(self):
        for key, value in PARAMETERS.items():
            try:
                form_creator = getattr(self, value["type"])
                form = form_creator(value)
                field_layout = self.create_field(value["label"], form)
                self.main_layout.addLayout(field_layout)
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
        form = form_class()
        form.setRange(minimum, maximum)
        form.setValue(value)
        return form

    def _choices_form(self, form_class, items, value):
        if value not in items:
            raise ValueError(
                f"Invalid value: {value}. Must be in items {items}.")
        form = form_class()
        form.addItems(items)
        form.setCurrentText(value)
        return form

    def show(self):
        self.generator()
        self.create_action_buttons()
        self.frame.raise_()
        self.frame.show()
