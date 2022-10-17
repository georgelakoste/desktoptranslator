from PyQt5.QtWidgets import QApplication
from ui import TranslatorWindow

if __name__ == "__main__":
    app = QApplication([])
    window = TranslatorWindow()
    window.show()
    app.exec()
