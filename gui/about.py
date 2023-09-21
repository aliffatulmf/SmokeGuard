from PySide6.QtWidgets import QWidget, QMessageBox

class AboutBox(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.info = QMessageBox()
        self.info.setText("About SmokeGuard")
        self.info.setParent(parent)

    def show(self):
        self.info.show()