import logging

import torch
from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QFont, QIcon
from PySide6.QtWidgets import (QHBoxLayout, QLabel, QScrollArea, QVBoxLayout,
                               QWidget)


class Layout(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowIcon(QIcon("assets/icon/icon.png"))
        self.scroll_widget = QWidget()
        self.scroll_area = QScrollArea()
        self.scroll_layout = QVBoxLayout()

        self.setWindowTitle("Snapshot Window")
        # self.setMinimumHeight(300)
        # self.setMinimumWidth(1200)

        self.scroll_widget = QWidget(self)
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_layout.setContentsMargins(30, 30, 0, 0)
        self.scroll_widget.setStyleSheet("background: #ffffff; border-radius: 10px;")

        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.scroll_widget)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.addWidget(self.scroll_area)

        self.__font = QFont()
        self.__font.setBold(True)
        self.__font.setPointSize(13)

    def add_label_to_layout(self, text, layout):
        label = QLabel(text)
        label.setFont(self.__font)
        label.setWordWrap(False)
        label.setStyleSheet("margin-top: 20px;")

        layout.addWidget(label)
        return label

    def label_value_pair(self, label_text, value_text, vl1, vl2):
        label = self.add_label_to_layout(label_text, vl1)
        value = self.add_label_to_layout(value_text, vl2)
        return label, value

    @staticmethod
    def horizontal_layout():
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        return layout

    @staticmethod
    def vertical_layout():
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        return layout


class SnapshotWindow(Layout):
    def __init__(self, maxlim):
        super().__init__()
        assert maxlim >= 0 and maxlim <= 100, "cannot set limit to more than 100 and lower than 0"

        if maxlim == 0:
            logging.warning("Unrestricted snapshot limit may cause memory leaks.")

        self.max_limit = maxlim
        self.widgets_list = []

    def remove_earlier_row(self):
        """
        Removes the earlier row from the widgets list and deletes the associated widgets and layouts.
        If the widgets list is empty, the function does nothing.

        Raises:
            IndexError: If trying to remove an item from an empty list.
        """
        if not self.widgets_list:
            return

        option = self.widgets_list.pop(0)

        # Remove frame widget
        image_frame = option["frame"]
        self.scroll_layout.removeWidget(image_frame)
        image_frame.deleteLater()

        # Remove info layout
        option["info"].deleteLater()

        # Remove main layout
        main_layout = option["main"]

        # Remove all widgets from the main layout
        for i in reversed(range(main_layout.count())):
            widget = main_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        self.scroll_layout.removeItem(main_layout)
        main_layout.deleteLater()

        # Remove vertical labels
        for label in option["labels"]:
            option["info"].removeWidget(label)
            label.deleteLater()

        for value in option["values"]:
            option["info"].removeWidget(value)
            value.deleteLater()

    def create_layouts(self, pixmap):
        main = self.horizontal_layout()
        info = self.horizontal_layout()
        left = self.vertical_layout()
        right = self.vertical_layout()

        # info.setContentsMargins(0, 0, 1500, 80)

        image = QLabel()
        image.setStyleSheet("padding-right: 30px;")
        image.setPixmap(pixmap)

        main.addWidget(image)
        info.addLayout(left)
        info.addLayout(right)
        main.addLayout(info)

        return main, left, right, image, info

    @staticmethod
    def extract_data_pairs(data):
        conf = f": {data['confidence'] * 100:.2f}% ({round(data['confidence'] * 100)}%)"
        conf_thres = f": {data['threshold']['confidence']} / {data['threshold']['iou']}"
        inf_time = f": {data['inference']['min']:.2f}ms [AVG {data['inference']['avg']:.2f}ms]"
        fps = f": {int(data['fps']['min'])} [AVG {int(data['fps']['avg'])}]"
        floating_point = {
            torch.float16: "FP16 [Half Precision]",
            torch.float32: "FP32 [Single Precision]",
            torch.float64: "FP64 [Double Precision]"
        }.get(data['floating_point'], "")

        dataset = [
            ("Confidence Average", conf),
            ("Confidence / IoU Threshold", conf_thres),
            ("Inference Time", inf_time),
            ("FPS", fps),
            ("Floating Point", f": {floating_point}"),
        ]

        return dataset

    def parse_labels_values(self, dataset, left, right):
        labels = []
        values = []
        for key, val in dataset:
            label, value = self.label_value_pair(key, val, left, right)
            labels.append(label)
            values.append(value)
        return labels, values

    @Slot()
    def signal_receiver(self, received_data):
        if self.scroll_layout.count() >= self.max_limit and self.max_limit != 0:
            self.remove_earlier_row()  # Remove earlier row

        main, left, right, image, info = self.create_layouts(received_data["image"]["qpixmap"])
        data_pairs = self.extract_data_pairs(received_data)
        label, value = self.parse_labels_values(data_pairs, left, right)

        widget_parameters = {
            "main": main,
            "info": info,
            "labels": label,
            "values": value,
            "frame": image,
        }

        self.scroll_layout.addLayout(main)
        self.widgets_list.append(widget_parameters)
