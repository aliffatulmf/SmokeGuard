from PySide6.QtWidgets import QWidget, QScrollArea, QLabel, QVBoxLayout, QHBoxLayout
from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QPixmap, QImage, QIcon

from classtype import ImageType


class SnapshotWindow(QWidget):
    def __init__(self) -> None:
        super(SnapshotWindow, self).__init__()
        self.setWindowIcon(QIcon("assets/icon/icon.png"))
        self.scroll_panel = None
        self.scroll_panel_layout = None
        self.scroll_area = None
        self.main_layout = None
        
        self.label_list = []

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Snapshot Window")
        self.setFixedHeight(900)
        self.setMinimumWidth(600)
        self.setMaximumWidth(900)

        self.scroll_panel = QWidget(self)
        
        self.scroll_panel_layout = QVBoxLayout(self.scroll_panel)
        self.scroll_panel_layout.setContentsMargins(30, 30, 0, 0)

        self.scroll_area = QScrollArea()
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        # Automatically scroll to the bottom of the scroll area when a new image is added
        self.scroll_area.verticalScrollBar().rangeChanged.connect(self._update_scroll)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.scroll_panel)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.addWidget(self.scroll_area)

    def _update_scroll(self, min, max):
        self.scroll_area.verticalScrollBar().setValue(max)

    def add_image(self, image: ImageType):
        h_layout = QHBoxLayout()
        h_layout.setContentsMargins(0, 0, 0, 0)
        h_layout.setSpacing(0)
        
        field_layout = QVBoxLayout()
        field_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        field_layout.setSpacing(5)
        
        name_label = QLabel(f"Name:\t\t{image.name}")
        conf_label = QLabel(f"Confidence:\t{image.confidence}")
        time_label = QLabel(f"Time:\t\t{image.timestamp}")
        
        field_layout.addWidget(name_label)
        field_layout.addWidget(conf_label)
        field_layout.addWidget(time_label)
        
        self.label_list.append((name_label, conf_label, time_label))
        
        pixmap = QPixmap(image.image)
        frame = QLabel()
        frame.setPixmap(pixmap.scaledToHeight(300))
        
        h_layout.addWidget(frame)
        h_layout.addLayout(field_layout)
        
        self.scroll_panel_layout.addLayout(h_layout)
        
        if self.scroll_panel_layout.count() > 100:
            scroll_widget = self.scroll_panel_layout.takeAt(0).widget()
            if scroll_widget:
                scroll_widget.deleteLater()
                
            label_list = self.label_list.pop(0)
            label_list[0].deleteLater()
            label_list[1].deleteLater()
            label_list[2].deleteLater()

    def add_pixmap(self, pixmap: QPixmap):
        label = QLabel()
        label.setPixmap(pixmap.scaled(300, 300))

        self.scroll_panel_layout.addRow(label)

    @Slot(QPixmap)
    def slot_pixmap(self, pixmap: QPixmap):
        self.add_pixmap(pixmap)

    @Slot(QImage)
    def slot_image(self, image: ImageType):
        self.add_image(image)
