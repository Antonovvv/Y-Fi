# -*- coding:utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys

from UI.ui_main import *
from GUI.model_page import ModelPage

from model import GLWindow, Building, Source


class Main(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        self.setupUi(self)

        self.add_event()

    def add_event(self):
        self.new_file.triggered.connect(self.new_model)

    def new_model(self):
        new_page = ModelPage()
        self.tabWidget.addTab(new_page, "new")

    def resizeEvent(self, e):
        self.tabWidget.resize(e.size().width(), e.size().height() - 40)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec_())
