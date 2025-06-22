from MainWindow import Ui_MainWindow
from PyQt6.QtWidgets import QMainWindow, QApplication
import sys

class MainWindowController(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


app = QApplication([])
mainWindow = MainWindowController()
mainWindow.show()
sys.exit(app.exec())
