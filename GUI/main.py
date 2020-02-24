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

        self.count = 0

        self.add_event()

    def add_event(self):
        self.new_file.triggered.connect(self.new_model)
        self.open_file.triggered.connect(self.open_model)
        self.save_file.triggered.connect(self.save_model)
        self.tabWidget.tabCloseRequested[int].connect(self.close_tab)

    def new_model(self):
        name = "untitled_" + str(self.count)
        new_page = ModelPage(name=name)
        self.tabWidget.addTab(new_page, name)
        self.count += 1
        self.save_file.setEnabled(True)

    def open_model(self):
        filepath, filetype = QFileDialog.getOpenFileName(self, '打开文件', '../saved', '仿真文件(*.yfi)')
        if filepath:
            with open(filepath, 'rb') as f:
                file = pickle.load(f)
                model = ModelPage(name=file['name'])
                model.glwindow.building = file['building']
                model.glwindow.sources = file['sources']
                self.tabWidget.addTab(model, file['name'])
            self.save_file.setEnabled(True)

    def save_model(self):
        filepath, filetype = QFileDialog.getSaveFileName(self, '保存文件', '../saved', '仿真文件(*.yfi)')
        filename = QFileInfo(filepath).baseName()
        self.tabWidget.setTabText(self.tabWidget.currentIndex(), filename)  # 改变当前tab标题
        target = self.tabWidget.currentWidget()
        target.name = filename
        with open(filepath, 'wb') as f:
            content = dict(name=target.name,
                           building=target.glwindow.building,
                           sources=target.glwindow.sources)
            pickle.dump(content, f)

    def close_tab(self, value):
        self.tabWidget.removeTab(value)
        if self.tabWidget.count() == 0:
            self.save_file.setEnabled(False)

    def resizeEvent(self, e):
        self.tabWidget.resize(e.size().width(), e.size().height() - 40)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec_())
