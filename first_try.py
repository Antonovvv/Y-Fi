# -*- coding:utf-8 -*-
# from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
# from OpenGL.GL import *
# from OpenGL.GLU import *
from OpenGL.GLUT import *

import numpy as np

from model import GLWindow


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__()
        self.base()

    def base(self):
        self.setWindowTitle('Controller')
        self.resize(320, 960)
        self.move(120, 120)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.MSWindowsFixedSizeDialogHint)

        self.statusBar()
        self.add_buttons()

    def add_buttons(self):
        start_btn = QPushButton('start', self)
        start_btn.resize(120, 60)
        start_btn.move(100, 80)
        start_btn.clicked.connect(self.start)

    def get_screen(self):
        # qr = self.frameGeometry()
        # cp = QDesktopWidget().availableGeometry().center()
        # qr.moveCenter(cp)
        # self.move(qr.topLeft())
        screen = QDesktopWidget().availableGeometry()
        return screen.width(), screen.height()

    def start(self):
        self.statusBar().showMessage('clicked')
        glwindow = GLWindow()
        glutInit()
        display_mode = GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH
        glutInitDisplayMode(display_mode)

        gl_width, gl_height = self.get_screen()
        glutInitWindowPosition(0, 0)
        glutInitWindowSize(gl_width, gl_height)
        glutCreateWindow('model')

        glwindow.init()
        glutDisplayFunc(glwindow.draw)
        glutReshapeFunc(glwindow.reshape)  # 注册响应窗口改变的函数reshape()
        glutMouseFunc(glwindow.mouse_click)  # 注册响应鼠标点击的函数
        glutMotionFunc(glwindow.mouse_motion)  # 注册响应鼠标拖拽的函数
        glutKeyboardFunc(glwindow.keydown)  # 注册键盘输入的函数keydown()
        glutMainLoop()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
