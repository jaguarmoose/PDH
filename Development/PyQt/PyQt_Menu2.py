import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenuBar, QAction, qApp

class Example(QMainWindow):

    def __init__(self):
        super().__init__()

        exitAction = QAction(QIcon('exit.png'), '&Exit', self)
        exitAction.triggered.connect(qApp.quit)
        menubar = QMenuBar()
        self.setMenuBar(menubar)
#        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&Testmenu')
        fileMenu.addAction(exitAction)

        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
