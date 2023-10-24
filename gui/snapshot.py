from typing import List

from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QFont, QIcon, QImage, QPixmap
from PySide6.QtWidgets import QHBoxLayout, QLabel, QScrollArea, QVBoxLayout, QWidget

from classtype import ImageType


class SnapshotWindow(QWidget):
    def __init__(self) -> None:
        super(SnapshotWindow, self).__init__()

        # Sets the window icon to be the specified image.
        self.setWindowIcon(QIcon("assets/icon/icon.png"))

        # Initialises the scroll panel widget.
        self.scrollWidget: QWidget = QWidget()

        # Initialises the scroll area widget.
        self.scrollArea: QScrollArea = QScrollArea()

        # Initialises the layout for the scroll panel.
        self.scrollLayout: QVBoxLayout = QVBoxLayout()

        # Main layout is initially set to None.
        self.mainLayout = None

        self.label_list: List[tuple[QLabel, QLabel, QLabel]] = []
        self.initialize_user_interface()

    def initialize_user_interface(self):
        self.setWindowTitle("Snapshot Window")
        self.setFixedHeight(600)
        self.setMinimumWidth(1000)
        self.setMaximumWidth(1080)

        self.scrollWidget = QWidget(self)
        self.scrollLayout = QVBoxLayout(self.scrollWidget)
        self.scrollLayout.setContentsMargins(30, 30, 0, 0)
        self.scrollWidget.setStyleSheet("background: #ffffff; border-radius: 10px;")

        self.scrollArea = QScrollArea()
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scrollArea.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        # Disable auto-scroll on the scroll area
        # self.scrollArea.verticalScrollBar().rangeChanged.connect(
        #     lambda min, max: self.scrollArea.verticalScrollBar().setValue(max)
        # )

        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.scrollWidget)

        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.addWidget(self.scrollArea)

    def add_image(self, input_image: ImageType):
        if self.scrollLayout.count() > 10:
            self.remove_first_widget()
            self.remove_first_label_set()

        horizontal_layout = self.create_horizontal_layout()
        horizontal_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        field_layout = self.create_vertical_layout()
        field_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        labels_to_add = self.create_labels(input_image)
        for label in labels_to_add:
            field_layout.addWidget(label)

        self.label_list.append(labels_to_add)

        image_frame = self.create_frame(input_image.image)
        horizontal_layout.addWidget(image_frame)
        horizontal_layout.addLayout(field_layout)

        self.scrollLayout.addLayout(horizontal_layout)

    def create_labels(self, image: ImageType) -> tuple[QLabel, QLabel, QLabel]:
        font = QFont()
        font.setStyleStrategy(QFont.StyleStrategy.PreferAntialias)
        font.setFamily("Segeo UI")
        font.setPixelSize(18)

        name_label = QLabel(f"Name:\t\t{image.name}")
        name_label.setFont(font)
        name_label.setWordWrap(True)

        conf_label = QLabel(f"Confidence:\t{image.confidence * 100:.2f}%")
        conf_label.setStyleSheet("font-size: 18px")
        conf_label.setFont(font)
        conf_label.setWordWrap(True)

        time_label = QLabel(f"Time:\t\t{image.timestamp}")
        time_label.setStyleSheet("font-size: 18px")
        time_label.setFont(font)
        time_label.setWordWrap(True)

        return (name_label, conf_label, time_label)

    def create_horizontal_layout(self):
        h_layout = QHBoxLayout()
        h_layout.setContentsMargins(0, 0, 0, 0)
        h_layout.setSpacing(0)
        return h_layout

    def create_vertical_layout(self):
        field_layout = QVBoxLayout()
        field_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        field_layout.setSpacing(5)
        return field_layout

    def create_frame(self, image):
        pixmap = QPixmap(image)
        frame = QLabel()
        frame.setPixmap(pixmap.scaledToHeight(300))
        return frame

    def remove_first_widget(self):
        first_widget = self.scrollLayout.takeAt(0)
        widget_to_remove = first_widget.widget()
        if widget_to_remove is not None:
            self.scrollLayout.removeWidget(widget_to_remove)
            widget_to_remove.deleteLater()

    def remove_first_label_set(self):
        first_label_set = self.label_list.pop(0)
        field_layout = self.scrollLayout.itemAt(0).layout()
        for label in first_label_set:
            field_layout.removeWidget(label)
            label.deleteLater()

    def add_pixmap(self, pixmap: QPixmap):
        label = QLabel()
        label.setPixmap(pixmap.scaled(300, 300))
        self.scrollLayout.addWidget(label)

    @Slot(QPixmap)
    def slot_pixmap(self, pixmap: QPixmap):
        self.add_pixmap(pixmap)

    @Slot(QImage)
    def slot_image(self, image: ImageType):
        self.add_image(image)
