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

from model import GLWindow, Building, Source


class Controller(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(Controller, self).__init__(parent)
        self.setupUi(self)
        # self.tabWidget.hide()
        self.sources = []
        self.add_event()

    def add_event(self):
        self.new_file.triggered.connect(self.new_model)

        self.spin_floors.valueChanged[int].connect(self.on_floors_changed)
        self.spin_rooms.valueChanged[int].connect(self.on_rooms_changed)
        self.spin_floor_thickness.valueChanged[float].connect(self.on_floor_thickness_changed)

        self.source_selector.activated[int].connect(self.on_source_selected)
        self.button_new_source.clicked.connect(self.new_source)

    def on_floors_changed(self, value):
        self.glwindow.building.floors = value
        self.glwindow.update()

    def on_rooms_changed(self, value):
        self.glwindow.building.rooms = value
        self.glwindow.update()

    def on_floor_thickness_changed(self, value):
        self.glwindow.building.floor_thickness = value
        self.glwindow.update()

    def on_source_selected(self, value):
        self.stackedWidget.setCurrentIndex(value + 1)

    def new_source(self):
        new = WifiController(self.glwindow)
        self.sources.append(1)

        self.source_selector.addItem('wifi_' + str(len(self.sources)))
        self.stackedWidget.addWidget(new)
        self.source_selector.setCurrentIndex(len(self.sources))
        self.stackedWidget.setCurrentIndex(len(self.sources) + 1)

    def new_model(self):
        # self.tabWidget.show()
        building = Building()
        self.glwindow = GLWindow(building)
        self.glwindow.setFocusPolicy(Qt.ClickFocus)
        self.model_view.addWidget(self.glwindow)
        self.model_view.setCurrentIndex(2)

    def resizeEvent(self, e):
        self.model_view.resize(e.size().width()-360, e.size().height())


class WifiController(QWidget, Ui_WifiBox):
    def __init__(self, glwindow, parent=None):
        super(WifiController, self).__init__(parent)
        self.setupUi(self)
        self.source = Source()
        self.glwindow = glwindow
        self.glwindow.sources.append(self.source)
        self.glwindow.update()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Controller()
    window.show()
    sys.exit(app.exec_())
