# -*- coding:utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys

from UI.ui_controller import *
from UI.ui_wifi import *

# from OpenGL.GL import *
# from OpenGL.GLU import *
from OpenGL.GLUT import *

import numpy as np

from model import GLWindow


class Controller(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(Controller, self).__init__(parent)
        self.setupUi(self)
        self.tabWidget.hide()
        self.glwindow = GLWindow()
        self.sources = []
        self.add_event()

    def add_event(self):
        self.new_file.triggered.connect(self.new_model)
        self.spin_floors.valueChanged[int].connect(self.on_floors_changed)
        self.source_selector.activated[int].connect(self.on_source_selected)
        self.button_new_source.clicked.connect(self.new_source)

    def on_floors_changed(self, value):
        self.glwindow.floors = value
        glutPostRedisplay()

    def on_source_selected(self, value):
        self.stackedWidget.setCurrentIndex(value + 1)

    def new_source(self):
        self.source_selector.addItem('wifi_' + str(len(self.sources)))
        new = WifiController()
        self.sources.append(1)
        self.stackedWidget.addWidget(new)
        self.source_selector.setCurrentIndex(len(self.sources))
        self.stackedWidget.setCurrentIndex(len(self.sources) + 1)

    def new_model(self):
        self.tabWidget.show()
        glutInit()
        display_mode = GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH
        glutInitDisplayMode(display_mode)

        # gl_width, gl_height = self.get_screen()
        glutInitWindowPosition(0, 0)
        # glutInitWindowSize(gl_width, gl_height)
        glutCreateWindow('model')

        self.glwindow.init()
        glutDisplayFunc(self.glwindow.draw)
        glutReshapeFunc(self.glwindow.reshape)      # 注册响应窗口改变的函数reshape()
        glutMouseFunc(self.glwindow.mouse_click)    # 注册响应鼠标点击的函数
        glutMotionFunc(self.glwindow.mouse_motion)  # 注册响应鼠标拖拽的函数
        glutKeyboardFunc(self.glwindow.keydown)     # 注册键盘输入的函数keydown()
        glutSpecialFunc(self.glwindow.move_wifi)
        glutMainLoop()


class WifiController(QWidget, Ui_WifiBox):
    def __init__(self, parent=None):
        super(WifiController, self).__init__(parent)
        self.setupUi(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Controller()
    window.show()
    sys.exit(app.exec_())
