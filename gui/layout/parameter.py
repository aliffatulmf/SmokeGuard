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

ENABLE = "Enable"
DISABLE = "Disable"
SWITCH = [ENABLE, DISABLE]

config_manager = ConfigManager()

PARAMETERS = {
    "confidence_threshold": {
        "type": "spinbox",
        "label": "Confidence Threshold",
        "minimum": 1,
        "maximum": 100,
        "value": config_manager.get("confidence_threshold"),
    },
    "iou_threshold": {
        "type": "spinbox",
        "label": "Overlap Threshold",
        "minimum": 1,
        "maximum": 100,
        "value": config_manager.get("iou_threshold"),
    },
    "automatic_mixed_precision": {
        "type": "dropdown",
        "label": "Automatic Mixed Precision",
        "items": SWITCH,
        "value": config_manager.get("automatic_mixed_precision"),
    },
    # "hardware_acceleration": {
    #     "type": "dropdown",
    #     "label": "Hardware Acceleration",
    #     "items": ["Automatic"],
    #     "value": config_manager.get("device"),
    #     "disabled": True,
    # },
    "use_agnostic_nms": {
        "type": "dropdown",
        "label": "Class-Agnostic NMS",
        "items": SWITCH,
        "value": config_manager.get("use_agnostic_nms"),
    },
    "enable_augmentation": {
        "type": "dropdown",
        "label": "Data Augmentation",
        "items": SWITCH,
        "value": config_manager.get("enable_augmentation"),
    },
}


class ConfigLayout:
    def __init__(self, parent: QWidget = None):
        self.parent = parent

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

    def saveValue(self):
        for key, value in PARAMETERS.items():
            form_value = self.__dict__[f"{key}_form"]
            if "disabled" not in value:
                config_manager.set(
                    key,
                    form_value.value()
                    if value["type"] == "spinbox"
                    else form_value.currentText() == ENABLE,
                )

        config_manager.save()
        self.saveNotificationBox()
        self.parent.close()

    @staticmethod
    def saveNotificationBox():
        message_box = QMessageBox()
        message_box.setIcon(QMessageBox.Icon.Information)
        message_box.setWindowTitle("Notification")
        message_box.setText("Application will quit to apply changes.")
        message_box.exec()

    def actionButton(self):
        save_btn = QPushButton()
        save_btn.setText("Save")
        save_btn.clicked.connect(lambda: self.saveValue())

        reset_btn = QPushButton()
        reset_btn.setText("Reset")

        self.top_vbox.addWidget(save_btn)
        self.top_vbox.addWidget(reset_btn)

    def show(self):
        """
        This method generates the parameter form and action buttons on the GUI.

        It first calls the `generator` method to create the form for each parameter defined in the PARAMETERS dictionary.
        Then it calls the `actionButton` method to create the 'Save' and 'Reset' buttons.

        This method does not return anything.
        """
        self.generator()
        self.actionButton()

    def generator(self):
        """
        This method generates the form for each parameter defined in the PARAMETERS dictionary.

        For each parameter, it checks the type of the parameter. If the type is 'spinbox', it creates a spinbox form with the specified minimum, maximum, and current value. If the type is 'dropdown', it creates a dropdown form with the specified items and current value. If the 'disabled' key is present and set to True, the form is disabled.

        The generated form and its corresponding label are then stored as attributes of the ParameterLayout object, with the key of the parameter appended with '_form' and '_label' respectively.

        This method does not return anything.
        """

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
