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
        self.tabWidget.hide()
        self.sources = []
        self.add_event()

    def add_event(self):
        self.new_file.triggered.connect(self.new_model)

        self.spin_floors.valueChanged[int].connect(self.on_floors_changed)
        self.spin_rooms.valueChanged[int].connect(self.on_rooms_changed)
        self.spin_floor_thickness.valueChanged[float].connect(self.on_floor_thickness_changed)

        self.spin_room_length.valueChanged[float].connect(self.on_room_length_changed)
        self.spin_room_width.valueChanged[float].connect(self.on_room_width_changed)
        self.spin_room_height.valueChanged[float].connect(self.on_room_height_changed)
        self.spin_wall_thickness.valueChanged[float].connect(self.on_wall_changed)

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

    def on_room_length_changed(self, value):
        self.glwindow.building.room_size[0] = value
        self.glwindow.update()

    def on_room_width_changed(self, value):
        self.glwindow.building.room_size[1] = value
        self.glwindow.update()

    def on_room_height_changed(self, value):
        self.glwindow.building.room_size[2] = value
        self.glwindow.update()

    def on_wall_changed(self, value):
        self.glwindow.building.wall_thickness = value
        self.glwindow.update()

    def on_source_selected(self, value):
        self.stackedWidget.setCurrentIndex(value + 1)
        self.glwindow.active_source = value - 1

    def new_source(self):
        new = WifiController(self.glwindow)
        self.sources.append(1)

        self.source_selector.addItem('wifi_' + str(len(self.sources)))
        self.stackedWidget.addWidget(new)
        self.source_selector.setCurrentIndex(len(self.sources))
        self.stackedWidget.setCurrentIndex(len(self.sources) + 1)

        self.glwindow.active_source = len(self.sources) - 1

    def new_model(self):
        self.tabWidget.show()
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
        self.index = len(glwindow.sources)
        self.glwindow.sources.append(self.source)
        self.glwindow.update()
        self.init_value()
        self.add_event()

    def init_value(self):
        power = self.source.power
        self.power_dbm.display(power)
        power_w = pow(10, power / 10)
        self.power_w.display(power_w)

        self.spin_x.setValue(self.glwindow.sources[self.index].position[0])
        self.spin_y.setValue(self.glwindow.sources[self.index].position[1])
        self.spin_z.setValue(self.glwindow.sources[self.index].position[2])

    def add_event(self):
        self.show_check.stateChanged.connect(self.on_show_changed)
        self.freq_selector.activated[int].connect(self.on_freq_changed)
        self.power_slider.valueChanged[int].connect(self.on_power_changed)

        self.spin_x.valueChanged[float].connect(self.on_pos_x_changed)
        self.spin_y.valueChanged[float].connect(self.on_pos_y_changed)
        self.spin_z.valueChanged[float].connect(self.on_pos_z_changed)

        self.glwindow.source_x_changed[float].connect(self.pos_x_changed)
        self.glwindow.source_y_changed[float].connect(self.pos_y_changed)
        self.glwindow.source_z_changed[float].connect(self.pos_z_changed)

    def on_show_changed(self, state):
        if state == Qt.Checked:
            self.glwindow.sources[self.index].show = True
        else:
            self.glwindow.sources[self.index].show = False
        self.glwindow.update()

    def on_freq_changed(self, value):
        self.glwindow.sources[self.index].freq_change(value)
        self.glwindow.update()

    def on_power_changed(self, value):
        self.glwindow.sources[self.index].power = value
        self.power_dbm.display(value)
        power = pow(10, value / 10)
        self.power_w.display(power)
        self.glwindow.update()

    # spin控制位置事件
    def on_pos_x_changed(self, value):
        self.glwindow.sources[self.index].position[0] = value
        self.glwindow.update()

    def on_pos_y_changed(self, value):
        self.glwindow.sources[self.index].position[1] = value
        self.glwindow.update()

    def on_pos_z_changed(self, value):
        self.glwindow.sources[self.index].position[2] = value
        self.glwindow.update()

    # 方向键控制位置绑定spin值
    def pos_x_changed(self, value):
        self.spin_x.setValue(value)

    def pos_y_changed(self, value):
        self.spin_y.setValue(value)

    def pos_z_changed(self, value):
        self.spin_z.setValue(value)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Controller()
    window.showMaximized()
    sys.exit(app.exec_())
