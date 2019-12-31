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
        self.glwindow = GLWindow()
        self.base()

    def base(self):
        self.init_window()

        # self.add_buttons()
        self.add_freq_selector()
        self.add_power_slider()
        self.show()

        # self.init_model()

    def init_window(self):
        self.setWindowTitle('Controller')
        self.resize(360, 960)
        self.move(0, 0)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.MSWindowsFixedSizeDialogHint)

        self.statusBar()

        menubar = self.menuBar()
        mode_menu = menubar.addMenu('控制')

        mode_model = QAction('模型', self)
        mode_menu.addAction(mode_model)

        mode_wifi = QAction('wifi', self)
        mode_menu.addAction(mode_wifi)

    '''def add_buttons(self):
        freq_btn = QPushButton('添加wifi', self)
        freq_btn.resize(120, 60)
        freq_btn.move(100, 80)
        freq_btn.clicked.connect(self.change_wifi)'''

    def add_freq_selector(self):
        label = QLabel('发射频段', self)
        label.resize(120, 40)
        label.move(40, 40)

        freq_selecter = QComboBox(self)
        freq_selecter.addItem('5GHz')
        freq_selecter.addItem('2.4GHz')

        freq_selecter.resize(120, 40)
        freq_selecter.move(160, 40)

        freq_selecter.activated[str].connect(self.on_freq_change)

    def add_power_slider(self):
        self.power_label = QLabel('发射功率:15dBm', self)
        self.power_label.resize(240, 40)
        self.power_label.move(40, 100)

        power_slider = QSlider(Qt.Horizontal, self)
        power_slider.setFocusPolicy(Qt.NoFocus)
        power_slider.setMinimum(10)
        power_slider.setMaximum(20)
        power_slider.setSingleStep(1)
        power_slider.setTickInterval(1)
        power_slider.setTickPosition(1)
        power_slider.resize(240, 40)
        power_slider.move(40, 160)
        power_slider.setValue(15)
        power_slider.valueChanged[int].connect(self.on_power_changed)

    def get_screen(self):
        # qr = self.frameGeometry()
        # cp = QDesktopWidget().availableGeometry().center()
        # qr.moveCenter(cp)
        # self.move(qr.topLeft())
        screen = QDesktopWidget().availableGeometry()
        return screen.width(), screen.height()

    def init_model(self):
        glutInit()
        display_mode = GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH
        glutInitDisplayMode(display_mode)

        gl_width, gl_height = self.get_screen()
        glutInitWindowPosition(0, 0)
        glutInitWindowSize(gl_width, gl_height)
        glutCreateWindow('model')
        # glutFullScreenToggle()

        self.glwindow.init()
        glutDisplayFunc(self.glwindow.draw)
        glutReshapeFunc(self.glwindow.reshape)      # 注册响应窗口改变的函数reshape()
        glutMouseFunc(self.glwindow.mouse_click)    # 注册响应鼠标点击的函数
        glutMotionFunc(self.glwindow.mouse_motion)  # 注册响应鼠标拖拽的函数
        glutKeyboardFunc(self.glwindow.keydown)     # 注册键盘输入的函数keydown()
        glutSpecialFunc(self.glwindow.move_wifi)
        glutMainLoop()

    def on_freq_change(self, text):
        # 切换wifi频段
        # self.glwindow.wifi_type = ~(self.glwindow.wifi_type & 1)
        if text == '5GHz':
            self.glwindow.wifi_type = 0
        elif text == '2.4GHz':
            self.glwindow.wifi_type = 1
        glutPostRedisplay()

    def on_power_changed(self, value):
        self.glwindow.power = value
        self.power_label.setText('发射功率:{}dBm'.format(value))
        glutPostRedisplay()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    # window.show()

    sys.exit(app.exec_())
