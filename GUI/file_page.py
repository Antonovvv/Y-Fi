# -*- coding:utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
# import sys

from UI.ui_file_page import *
from GUI.source_control import SourceControl

from model import GLWindow, Building, Source
from ext import Watcher


class FilePage(QWidget, Ui_FilePage, Watcher):
    file_modified = pyqtSignal()    # 需定义在构造方法外！

    def __init__(self, glwindow, name='', parent=None):
        super(FilePage, self).__init__(parent)
        self.setupUi(self)
        self.name = name
        self.path = ''

        self.glwindow = glwindow
        self.glwindow.setFocusPolicy(Qt.ClickFocus)

        self.model_view.addWidget(self.glwindow)
        self.model_view.setCurrentIndex(0)
        self.source_count = 0

        self.init_value()
        self.add_event()

    def init_value(self):
        building = self.glwindow.building
        self.spin_floors.setValue(building.floors)
        self.spin_rooms.setValue(building.rooms)
        self.spin_floor_thickness.setValue(building.floor_thickness)

        self.spin_room_length.setValue(building.room_size[0])
        self.spin_room_width.setValue(building.room_size[1])
        self.spin_room_height.setValue(building.room_size[2])
        self.spin_wall_thickness.setValue(building.wall_thickness)

    def add_event(self):
        self.spin_floors.valueChanged[int].connect(self.on_floors_changed)
        self.spin_rooms.valueChanged[int].connect(self.on_rooms_changed)
        self.spin_floor_thickness.valueChanged[float].connect(self.on_floor_thickness_changed)

        self.spin_room_length.valueChanged[float].connect(self.on_room_length_changed)
        self.spin_room_width.valueChanged[float].connect(self.on_room_width_changed)
        self.spin_room_height.valueChanged[float].connect(self.on_room_height_changed)
        self.spin_wall_thickness.valueChanged[float].connect(self.on_wall_changed)

        self.glwindow.source_x_changed[float].connect(self.pos_x_changed)
        self.glwindow.source_y_changed[float].connect(self.pos_y_changed)
        self.glwindow.source_z_changed[float].connect(self.pos_z_changed)
        self.source_selector.activated[int].connect(self.on_source_selected)
        self.new_source_button.clicked.connect(self.new_source)

    @Watcher.watch_modify
    def on_floors_changed(self, value):
        self.glwindow.building.floors = value
        self.glwindow.update()

    @Watcher.watch_modify
    def on_rooms_changed(self, value):
        self.glwindow.building.rooms = value
        self.glwindow.update()

    @Watcher.watch_modify
    def on_floor_thickness_changed(self, value):
        self.glwindow.building.floor_thickness = value
        self.glwindow.update()

    @Watcher.watch_modify
    def on_room_length_changed(self, value):
        self.glwindow.building.room_size[0] = value
        self.glwindow.update()

    @Watcher.watch_modify
    def on_room_width_changed(self, value):
        self.glwindow.building.room_size[1] = value
        self.glwindow.update()

    @Watcher.watch_modify
    def on_room_height_changed(self, value):
        self.glwindow.building.room_size[2] = value
        self.glwindow.update()

    @Watcher.watch_modify
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

    @Watcher.watch_modify
    def new_source(self, e):
        self.glwindow.sources.append(Source())  # 新建信号源实例
        self.glwindow.update()

        index = self.stackedWidget.count()
        new = SourceControl(index, self.glwindow, self)
        self.stackedWidget.addWidget(new)
        self.source_selector.addItem('wifi_' + str(self.source_count))
        self.source_count += 1

        self.source_selector.setCurrentIndex(index)
        self.stackedWidget.setCurrentIndex(index)

        self.stackedWidget.widget(index).source_delete.connect(self.on_source_delete)
        self.stackedWidget.widget(index).source_modified.connect(self.on_modified)
        self.glwindow.active_source = index

    def open_init(self, sources):    # 打开文件后的初始化
        self.glwindow.sources = sources
        self.glwindow.active_source = 0
        for index, source in enumerate(sources):
            old = SourceControl(index, self.glwindow, self)
            self.stackedWidget.addWidget(old)
            self.source_selector.addItem('wifi_' + str(index))
            self.stackedWidget.widget(index).source_delete.connect(self.on_source_delete)
            self.stackedWidget.widget(index).source_modified.connect(self.on_modified)
        self.source_count = len(sources)

    def on_modified(self):
        self.file_modified.emit()

    def on_saved(self):
        self.modified = False
        for i in range(self.stackedWidget.count()):
            self.stackedWidget.widget(i).on_saved()

    def resizeEvent(self, e):
        self.model_view.resize(e.size().width()-360, e.size().height())
