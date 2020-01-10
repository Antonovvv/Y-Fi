# -*- coding:utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
import pickle

from UI.ui_main import *
from GUI.model_page import ModelPage

from model import GLWindow, Building, Source


class Main(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        self.setupUi(self)

        self.name = 0

        self.add_event()

    def add_event(self):
        self.new_file.triggered.connect(self.new_model)
        self.save_file.triggered.connect(self.save_model)
        self.tabWidget.tabCloseRequested[int].connect(self.close_tab)

    def new_model(self):
        name = "untitled_" + str(self.name)
        new_page = ModelPage(name=name)
        self.tabWidget.addTab(new_page, name)
        self.name += 1

    def save_model(self):
        with open('../saved/a.pk', 'wb') as f:
            pickle.dump(self.name, f)
        with open('../saved/a.pk', 'rb') as f:
            print(pickle.load(f))

    def close_tab(self, value):
        self.tabWidget.removeTab(value)

    def resizeEvent(self, e):
        self.tabWidget.resize(e.size().width(), e.size().height() - 40)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec_())
