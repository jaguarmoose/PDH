"""Test"""
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon


class Example(QMainWindow):
    """test"""

    def __init__(self):
        """Test"""
        super().__init__()

        self.initUI()


    def initUI(self):
        """test"""
        textEdit = QTextEdit()
        self.setCentralWidget(textEdit)

        exitAction = QAction(QIcon('exit24.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)

        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)

        toolbar = self.addToolBar('Exit')
        toolbar.addAction(exitAction)
        toolbar.setToolButtonStyle(1)

        self.setGeometry(300, 300, 350, 250)
        self.setWindowTitle('Main window')
        self.show()

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
#This code example creates a skeleton of a classic GUI application with a menubar, toolbar, and a statusbar.

    # textEdit = QTextEdit()
    # self.setCentralWidget(textEdit)