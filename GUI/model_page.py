# -*- coding:utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
# import sys

from UI.ui_model_page import *
from GUI.source_control import SourceControl

from model import GLWindow, Building


class ModelPage(QWidget, Ui_ModelPage):
    def __init__(self, name='', parent=None):
        super(ModelPage, self).__init__(parent)
        self.setupUi(self)
        self.name = name

        building = Building()
        self.glwindow = GLWindow(building)
        self.glwindow.setFocusPolicy(Qt.ClickFocus)
        self.model_view.addWidget(self.glwindow)
        self.model_view.setCurrentIndex(0)

        self.glwindow.source_x_changed[float].connect(self.pos_x_changed)
        self.glwindow.source_y_changed[float].connect(self.pos_y_changed)
        self.glwindow.source_z_changed[float].connect(self.pos_z_changed)
        self.source_count = 0

        self.add_event()

    def add_event(self):
        self.spin_floors.valueChanged[int].connect(self.on_floors_changed)
        self.spin_rooms.valueChanged[int].connect(self.on_rooms_changed)
        self.spin_floor_thickness.valueChanged[float].connect(self.on_floor_thickness_changed)

        self.spin_room_length.valueChanged[float].connect(self.on_room_length_changed)
        self.spin_room_width.valueChanged[float].connect(self.on_room_width_changed)
        self.spin_room_height.valueChanged[float].connect(self.on_room_height_changed)
        self.spin_wall_thickness.valueChanged[float].connect(self.on_wall_changed)

        self.source_selector.activated[int].connect(self.on_source_selected)
        self.new_source_button.clicked.connect(self.new_source)

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

    # 方向键控制信号源位置绑定spin值
    def pos_x_changed(self, value):
        active = self.glwindow.active_source
        self.stackedWidget.widget(active).spin_x.setValue(value)

    def pos_y_changed(self, value):
        active = self.glwindow.active_source
        self.stackedWidget.widget(active).spin_y.setValue(value)

    def pos_z_changed(self, value):
        active = self.glwindow.active_source
        self.stackedWidget.widget(active).spin_z.setValue(value)

    def on_source_selected(self, value):
        self.stackedWidget.setCurrentIndex(value)
        self.glwindow.active_source = value

    def on_source_delete(self):
        index = self.stackedWidget.currentIndex()

        self.glwindow.sources.pop(index)
        self.stackedWidget.removeWidget(self.stackedWidget.widget(index))
        self.source_selector.removeItem(index)
        self.glwindow.active_source = self.stackedWidget.currentIndex()

        self.glwindow.update()

    def new_source(self):
        index = self.stackedWidget.count()

        new = SourceControl(index, self.glwindow, self)
        self.stackedWidget.addWidget(new)
        self.source_selector.addItem('wifi_' + str(self.source_count))
        self.source_count += 1

        self.source_selector.setCurrentIndex(index)
        self.stackedWidget.setCurrentIndex(index)

        self.stackedWidget.widget(index).source_delete.connect(self.on_source_delete)
        self.glwindow.active_source = index

    def resizeEvent(self, e):
        self.model_view.resize(e.size().width()-360, e.size().height())
