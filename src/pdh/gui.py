'''QT 5 GUI'''
import sys
from PyQt5.QtWidgets import QApplication, QWidget


def build_window(title="PDH", size=(250, 150), position=(300, 300)):
    """Create and return the main PDH widget."""
    w = QWidget()
    w.resize(*size)
    w.move(*position)
    w.setWindowTitle(title)
    return w


def main():
    """Launch the basic PDH Qt window."""
    app = QApplication(sys.argv)
    w = build_window()
    w.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
