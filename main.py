import sys
from PySide6.QtWidgets import QApplication
from app import MainWindow
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("PVC Card Studio V3")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
