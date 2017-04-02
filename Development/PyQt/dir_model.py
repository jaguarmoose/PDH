import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import *


if __name__ == '__main__':


    app = QApplication(sys.argv)

    model = QDirModel()
    tree = QTreeView()
    tree.setModel(model)

    tree.setAnimated(False)
    tree.setIndentation(20)
    tree.setSortingEnabled(True)

    tree.setWindowTitle("Dir View")
    tree.resize(640, 480)
    tree.show()

    sys.exit(app.exec_())