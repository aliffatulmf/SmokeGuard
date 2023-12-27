from typing import List

from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QFont, QIcon, QImage, QPixmap
from PySide6.QtWidgets import (QHBoxLayout, QLabel, QScrollArea, QVBoxLayout,
                               QWidget)


class SnapshotWindow(QWidget):
    index = 1

    def __init__(self) -> None:
        super().__init__()
        self.setWindowIcon(QIcon("assets/icon/icon.png"))
        self.scrollWidget = QWidget()
        self.scrollArea = QScrollArea()
        self.scrollLayout = QVBoxLayout()

        self.mainLayout = None
        self.label_list: List[tuple[QLabel, QLabel, QLabel]] = []
        self.initialize_user_interface()
    
    @classmethod
    def index_add(cls):
        cls.index += 1

    def initialize_user_interface(self):
        self.setWindowTitle("Snapshot Window")
        self.setFixedHeight(600)
        self.setMinimumWidth(1200)
        self.setMaximumWidth(1380)

        self.scrollWidget = QWidget(self)
        self.scrollLayout = QVBoxLayout(self.scrollWidget)
        self.scrollLayout.setContentsMargins(30, 30, 0, 0)
        self.scrollWidget.setStyleSheet("background: #ffffff; border-radius: 10px;")

        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.scrollWidget)

        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.addWidget(self.scrollArea)

    def add_image(self, metadata):
        # Remove the first widget and labels if the number of widgets exceeds 10
        # if self.scrollLayout.count() > 10:
        #     self.remove_first_widget_and_labels()

        horizontal_layout = QHBoxLayout()
        horizontal_layout.setAlignment(Qt.AlignVCenter)

        font = QFont()
        font.setStyleStrategy(QFont.StyleStrategy.PreferAntialias)
        font.setFamily("Segeo UI")
        font.setPixelSize(18)

        index_label = QLabel(f"{self.index}.")
        index_label.setFont(font)
        index_label.setFixedWidth(30)
        self.index_add()

        name_label = QLabel(f"Name: {metadata.image_name}")
        name_label.setFont(font)
        name_label.setWordWrap(True)

        conf_label = QLabel(
            f"Confidence: {metadata.confidence_score * 100:.2f}%")
        conf_label.setFont(font)
        conf_label.setWordWrap(True)

        # Format the timestamp to a shorter format, e.g., "12 Dec 15:45"
        time_label = QLabel(
            f"Time: {metadata.image_timestamp.strftime('%d %b %H:%M:%S')}")
        time_label.setFont(font)
        time_label.setWordWrap(False)

        labels_to_add = (index_label, name_label, conf_label, time_label)
        for label in labels_to_add:
            horizontal_layout.addWidget(label)
        self.label_list.append(labels_to_add)

        pixmap = QPixmap(metadata.image_data)
        frame = QLabel()
        frame.setPixmap(pixmap.scaledToHeight(600))
        horizontal_layout.addWidget(frame)

        self.scrollLayout.addLayout(horizontal_layout)

    def remove_first_widget_and_labels(self):
        first_widget = self.scrollLayout.takeAt(0).widget()
        if first_widget is not None:
            self.scrollLayout.removeWidget(first_widget)
            first_widget.deleteLater()

        first_label_set = self.label_list.pop(0)
        for label in first_label_set:
            label.deleteLater()

    @Slot(QPixmap)
    def slot_pixmap(self, pixmap: QPixmap):
        label = QLabel()
        label.setPixmap(pixmap.scaled(300, 300))
        self.scrollLayout.addWidget(label)

    @Slot(QImage)
    def slot_image(self, image):
        self.add_image(image)
