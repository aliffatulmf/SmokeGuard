import torch
from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (QHBoxLayout, QLabel, QScrollArea, QVBoxLayout,
                               QWidget)

from meta import CONFIG_READ
from meta.io import Font
from meta.signal import SnapshotNamespace


class Layout(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowIcon(QIcon("assets/icon/icon.png"))
        self.scrollWidget = QWidget()
        self.scrollArea = QScrollArea()
        self.scrollLayout = QVBoxLayout()

        self.setWindowTitle("Snapshot Window")
        self.setMinimumHeight(300)
        self.setMinimumWidth(1200)

        self.font_mono = Font()

        self.scrollWidget = QWidget(self)
        self.scrollLayout = QVBoxLayout(self.scrollWidget)
        self.scrollLayout.setContentsMargins(30, 30, 0, 0)
        self.scrollWidget.setStyleSheet("background: #ffffff; border-radius: 10px;")

        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.scrollWidget)

        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.addWidget(self.scrollArea)
        
    def add_label_to_layout(self, text, layout):
        label = QLabel(text)
        label.setFont(self.font_mono)
        label.setWordWrap(False)
        label.setStyleSheet("margin-top: 20px;")
        layout.addWidget(label)
        return label

    def label_value_pair(self, label_text, value_text, vl1, vl2):
        label = self.add_label_to_layout(label_text, vl1)
        value = self.add_label_to_layout(value_text, vl2)
        return label, value

    def horizontal_layout(self):
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        return layout

    def vertical_layout(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        return layout


class SnapshotWindow(Layout):
    def __init__(self) -> None:
        super().__init__()

        self.widgetsList = []
    
    def delete_widgets_from_layout(self, layout):
        for i in reversed(range(layout.count())):
            widget = layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()
    
    def remove_first_widget(self):
        if not self.widgetsList:
            return

        widget_dict = self.widgetsList.pop(0)

        # Remove frame
        frame = widget_dict["image_frame"]
        self.scrollLayout.removeWidget(frame)
        frame.deleteLater()

        # Remove widgets from vertical_layouts
        for layout in widget_dict["vertical_layouts"]:
            self.delete_widgets_from_layout(layout)

        # Remove all widgets from the hlayout and then remove hlayout
        hl = widget_dict["horizontal_layout"]
        self.delete_widgets_from_layout(hl)
        self.scrollLayout.removeItem(hl)
        hl.deleteLater()

        # Remove vlabels
        for label in widget_dict["vertical_labels"]:
            # Assuming you want to delete these labels
            label.deleteLater()
    
    def create_layouts_frame(self, pixmap):
        horizontal_layout = self.horizontal_layout()
        vertical_layout1 = self.vertical_layout()
        vertical_layout2 = self.vertical_layout()

        frame = QLabel()
        frame.setStyleSheet("padding-right: 30px;")
        frame.setPixmap(pixmap)

        horizontal_layout.addLayout(vertical_layout1)
        horizontal_layout.addLayout(vertical_layout2)
        horizontal_layout.addWidget(frame)

        return vertical_layout1, vertical_layout2, horizontal_layout, frame

    def extract_data_pairs(self, data):
        dataset = [
            ("Confidence", f": {data.confidence * 100:.3f}% ({round(data.confidence * 100)}%)"),
            ("Confidence / IoU Threshold", f": {data.confidence_threshold} / {data.iou_threshold}"),
            ("Inference Time", f": {data.inference_time[0]:.2f}ms [AVG {data.inference_time[3]:.2f}ms]"),
            ("Frames Per Second", f": {int(data.fps[0])} [AVG {int(data.fps[3])}]"),
            (f"Accelerator [{data.accelerator}]", f": {data.hw_brand}"),
            ("Augmentation", f": {'Enabled' if CONFIG_READ['augment'] else 'Disabled'}"),
            # ("Automatic Mixed Precision", f": {'Enabled' if CONFIG_READ['amp'] else 'Disabled'}"),
        ]

        float_label = {
            torch.float16: "FP16 [Half Precision]",
            torch.float32: "FP32 [Single Precision]",
            torch.float64: "FP64 [Double Precision]"
        }.get(data.floating_point, "")

        dataset.append(("Floating Point", f": {float_label}"))

        return dataset

    def parse_labels_values(self, label_value_pairs, layout_1, layout_2):
        labels = []
        values = []
        for label_text, value_text in label_value_pairs:
            label, value = self.label_value_pair(label_text, value_text, layout_1, layout_2)
            labels.append(label)
            values.append(value)
        return labels, values

    def create_widget_parameter(self, vertical_layout1, vertical_layout2, horizontal_layout, frame, labels, values):
        return {
            "horizontal_layout": horizontal_layout,
            "vertical_layouts": [vertical_layout1, vertical_layout2],
            "vertical_labels": labels,
            "vertical_values": values,
            "image_frame": frame
        }

    @Slot(SnapshotNamespace)
    def signal_receiver(self, received_data):
        if self.scrollLayout.count() >= 50:
            self.remove_first_widget()

        layout1, layout2, horizontal_layout, image_frame = self.create_layouts_frame(received_data.pixmap)
        data_pairs = self.extract_data_pairs(received_data)
        label, value = self.parse_labels_values(data_pairs, layout1, layout2)
        widget_parameters = self.create_widget_parameter(layout1, layout2, horizontal_layout, image_frame, label, value)

        self.scrollLayout.addLayout(horizontal_layout)
        self.widgetsList.append(widget_parameters)
