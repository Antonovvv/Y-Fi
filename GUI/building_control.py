# -*- coding:utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from UI.ui_building_control import Ui_BuildingControl
from ext import Watcher


class BuildingControl(QWidget, Ui_BuildingControl, Watcher):
    building_delete = pyqtSignal()
    building_modified = pyqtSignal()

    def __init__(self, index, glwindow, parent=None):
        super(BuildingControl, self).__init__(parent)
        self.setupUi(self)

        self.glwindow = glwindow
        self.building = glwindow.buildings[index]

        self.init_value()
        self.add_event()

    def init_value(self):
        self.spin_floors.setValue(self.building.floors)
        self.spin_rooms.setValue(self.building.rooms)
        self.spin_floor_thickness.setValue(self.building.floor_thickness)

        self.spin_room_length.setValue(self.building.room_size[0])
        self.spin_room_width.setValue(self.building.room_size[1])
        self.spin_room_height.setValue(self.building.room_size[2])
        self.spin_wall_thickness.setValue(self.building.wall_thickness)

        self.spin_rotate.setValue(self.building.rotate)
        self.spin_x.setValue(self.building.position[0])
        self.spin_y.setValue(self.building.position[1])
        self.spin_z.setValue(self.building.position[2])

        self.show_check.setChecked(self.building.show)
        self.lock_check.setChecked(not self.building.enable)
        self.enable_all(self.building.enable)

    def add_event(self):
        self.show_check.stateChanged.connect(self.on_show_changed)
        self.lock_check.stateChanged.connect(self.on_lock_changed)
        self.delete_button.clicked.connect(self.delete)
        self.spin_floors.valueChanged[int].connect(self.on_floors_changed)
        self.spin_rooms.valueChanged[int].connect(self.on_rooms_changed)
        self.spin_floor_thickness.valueChanged[float].connect(self.on_floor_thickness_changed)

        self.spin_room_length.valueChanged[float].connect(self.on_room_length_changed)
        self.spin_room_width.valueChanged[float].connect(self.on_room_width_changed)
        self.spin_room_height.valueChanged[float].connect(self.on_room_height_changed)
        self.spin_wall_thickness.valueChanged[float].connect(self.on_wall_changed)

        self.spin_rotate.valueChanged[int].connect(self.on_rotate)
        self.spin_x.valueChanged[float].connect(self.on_pos_x_changed)
        self.spin_y.valueChanged[float].connect(self.on_pos_y_changed)
        self.spin_z.valueChanged[float].connect(self.on_pos_z_changed)

    @Watcher.watch_modify
    def on_show_changed(self, state):
        if state == Qt.Checked:
            self.building.show = True
            self.lock_check.setChecked(False)   # 显示时默认解锁
        else:
            self.building.show = False
            self.lock_check.setChecked(True)    # 不显示时默认锁定
        self.glwindow.update()

    @Watcher.watch_modify
    def on_lock_changed(self, state):
        if state == Qt.Checked:
            self.building.enable = False
            self.enable_all(False)
        else:
            self.building.enable = True
            self.enable_all(True)

    def enable_all(self, enable):
        self.delete_button.setEnabled(enable)
        self.spin_floors.setEnabled(enable)
        self.spin_rooms.setEnabled(enable)
        self.spin_floor_thickness.setEnabled(enable)

        self.spin_room_length.setEnabled(enable)
        self.spin_room_width.setEnabled(enable)
        self.spin_room_height.setEnabled(enable)
        self.spin_wall_thickness.setEnabled(enable)

        self.spin_rotate.setEnabled(enable)
        self.spin_x.setEnabled(enable)
        self.spin_y.setEnabled(enable)
        self.spin_z.setEnabled(enable)

    @Watcher.watch_modify
    def delete(self, e):
        self.building_delete.emit()

    # spin控制旋转
    @Watcher.watch_modify
    def on_rotate(self, value):
        self.building.rotate = value
        self.glwindow.update()

    # spin控制位置事件,也可由方向键控制触发
    @Watcher.watch_modify
    def on_pos_x_changed(self, value):
        self.building.position[0] = value
        self.glwindow.update()

    @Watcher.watch_modify
    def on_pos_y_changed(self, value):
        self.building.position[1] = value
        self.glwindow.update()

    @Watcher.watch_modify
    def on_pos_z_changed(self, value):
        self.building.position[2] = value
        self.glwindow.update()

    @Watcher.watch_modify
    def on_floors_changed(self, value):
        self.building.floors = value
        self.glwindow.update()

    @Watcher.watch_modify
    def on_rooms_changed(self, value):
        self.building.rooms = value
        self.glwindow.update()

    @Watcher.watch_modify
    def on_floor_thickness_changed(self, value):
        self.building.floor_thickness = value
        self.glwindow.update()

    @Watcher.watch_modify
    def on_room_length_changed(self, value):
        self.building.room_size[0] = value
        self.glwindow.update()

    @Watcher.watch_modify
    def on_room_width_changed(self, value):
        self.building.room_size[1] = value
        self.glwindow.update()

    @Watcher.watch_modify
    def on_room_height_changed(self, value):
        self.building.room_size[2] = value
        self.glwindow.update()

    @Watcher.watch_modify
    def on_wall_changed(self, value):
        self.building.wall_thickness = value
        self.glwindow.update()

    def on_modified(self):
        self.building_modified.emit()

    def on_saved(self):
        self.modified = False
