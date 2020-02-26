# -*- coding:utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
import pickle

from UI.ui_main import *
from GUI.file_page import FilePage

from model import GLWindow, Building


class Main(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        self.setupUi(self)

        self.count = 0

        self.add_event()

    def add_event(self):
        self.new_file.triggered.connect(self.on_new)
        self.open_file.triggered.connect(self.on_open)
        self.save_file.triggered.connect(self.on_save)
        self.save_as.triggered.connect(self.on_save_as)

        self.tabWidget.tabCloseRequested[int].connect(self.close_tab)

    def on_new(self):
        name = "untitled_" + str(self.count)
        new_glwindow = GLWindow(Building())     # 新建building实例，作为新建glwindow实例的参数
        new_page = FilePage(name=name, glwindow=new_glwindow)
        self.tabWidget.addTab(new_page, name)
        self.tabWidget.setCurrentWidget(new_page)
        self.tabWidget.currentWidget().file_modified.connect(self.on_file_modified)  # 文件改动事件
        self.count += 1

        self.save_file.setEnabled(True)
        self.save_as.setEnabled(True)

    def on_open(self):
        filepath, filetype = QFileDialog.getOpenFileName(self, '打开文件', '../saved', '仿真文件(*.yfi)')
        if filepath:
            for i in range(self.tabWidget.count()):
                if filepath == self.tabWidget.widget(i).path:
                    self.tabWidget.setCurrentIndex(i)   # 若文件已打开，则置为当前窗口
                    return
            with open(filepath, 'rb') as f:
                file = pickle.load(f)
            glwindow = GLWindow(building=file['building'])
            model = FilePage(name=file['name'], glwindow=glwindow)
            model.open_init(sources=file['sources'])
            model.path = filepath
            self.tabWidget.addTab(model, file['name'])
            self.tabWidget.setCurrentWidget(model)
            self.tabWidget.currentWidget().file_modified.connect(self.on_file_modified)
            self.save_file.setEnabled(True)
            self.save_as.setEnabled(True)

    def on_save(self):
        target = self.tabWidget.currentWidget()
        if not target.path == '':   # 当前为已存在文件，直接保存
            self.save_to(target=target, path=target.path)
        else:   # 当前为新文件，同另存为
            filepath, filetype = QFileDialog.getSaveFileName(self, '保存到', '../saved', '仿真文件(*.yfi)')
            if filepath:
                filename = QFileInfo(filepath).baseName()
                target.name = filename
                target.path = filepath
                self.save_to(target=target, path=filepath)

    def on_save_as(self):
        target = self.tabWidget.currentWidget()
        filepath, filetype = QFileDialog.getSaveFileName(self, '另存为', '../saved', '仿真文件(*.yfi)')
        if filepath:
            filename = QFileInfo(filepath).baseName()
            target.name = filename
            self.save_to(target=target, path=filepath)

    def save_to(self, target, path):
        with open(path, 'wb') as f:
            content = dict(name=target.name,
                           building=target.glwindow.building,
                           sources=target.glwindow.sources)
            pickle.dump(content, f)
        target.on_saved()
        self.tabWidget.setTabText(self.tabWidget.currentIndex(), target.name)  # 改变当前tab标题

    def on_file_modified(self):
        index = self.tabWidget.currentIndex()
        self.tabWidget.setTabText(index, self.tabWidget.widget(index).name + '*')   # 表示当前文件有改动，未保存

    def close_tab(self, value):
        self.tabWidget.removeTab(value)
        if self.tabWidget.count() == 0:
            self.save_file.setEnabled(False)
            self.save_as.setEnabled(False)

    def resizeEvent(self, e):
        self.tabWidget.resize(e.size().width(), e.size().height() - 40)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec_())
