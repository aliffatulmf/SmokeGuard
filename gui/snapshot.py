from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QFont, QIcon
from PySide6.QtWidgets import (QHBoxLayout, QLabel, QScrollArea, QVBoxLayout,
                               QWidget)

from meta.signal import SnapshotNamespace


class SnapshotWindow(QWidget):
    FONT = QFont()
    FONT.setStyleStrategy(QFont.StyleStrategy.PreferAntialias)
    FONT.setFamily("Segeo UI")
    FONT.setPixelSize(14)

    def __init__(self) -> None:
        super().__init__()
        self.setWindowIcon(QIcon("assets/icon/icon.png"))
        self.scrollWidget = QWidget()
        self.scrollArea = QScrollArea()
        self.scrollLayout = QVBoxLayout()

        self.setWindowTitle("Snapshot Window")
        self.setMinimumHeight(300)
        self.setMinimumWidth(1200)

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

        self.listed_widgets = []

    def create_label_and_add_to_layout(self, text, layout):
        label = self.create_label(text)
        label.setStyleSheet("margin-top: 20px;")
        layout.addWidget(label)
        return label

    def create_label_value_pair(self, label_text, value_text, vl1, vl2):
        label = self.create_label_and_add_to_layout(label_text, vl1)
        value = self.create_label_and_add_to_layout(value_text, vl2)
        return label, value
    

    def create_horizontal_layout(self):
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        return layout

    def create_vertical_layout(self):
        layout = QVBoxLayout()
        # layout.setSpacing(10)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        return layout

    def create_label(self, text):
        label = QLabel(text)
        label.setFont(self.FONT)
        label.setWordWrap(False)
        return label
    
    def delete_widgets_from_layout(self, layout):
        for i in reversed(range(layout.count())):
            widget = layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()
    
    def remove_first_widget(self):
        if not self.listed_widgets:
            return

        widget_dict = self.listed_widgets.pop(0)

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
    
    @Slot(SnapshotNamespace)
    def signal_receiver(self, data):
        if self.scrollLayout.count() >= 50:
            self.remove_first_widget()

        hl = self.create_horizontal_layout()
        vl1 = self.create_vertical_layout()
        vl2 = self.create_vertical_layout()

        labels_and_values = [
            ("Confidence:", f"{data.confidence * 100:.3f}% ({round(data.confidence * 100)}%)"),
            ("Confidence / IoU Threshold:", f"{data.confidence_threshold} / {data.iou_threshold}"),
            ("Inference Time:", f"{data.inference_time[0]:.2f} ms"),
            ("Frame Per Second:", f"{data.fps[0]:.1f}"),
        ]

        labels = []
        values = []
        for label_text, value_text in labels_and_values:
            label, value = self.create_label_value_pair(label_text, value_text, vl1, vl2)
            labels.append(label)
            values.append(value)

        frame = QLabel()
        frame.setStyleSheet("padding-right: 30px;")
        frame.setPixmap(data.pixmap)

        hl.addLayout(vl1)
        hl.addLayout(vl2)
        hl.addWidget(frame)

        self.scrollLayout.addLayout(hl)

        widget_dict = {
            "horizontal_layout": hl,
            "vertical_layouts": [vl1, vl2],
            "vertical_labels": labels,
            "vertical_values": values,
            "image_frame": frame
        }

        self.listed_widgets.append(widget_dict)