# -*- coding:utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
# import sys

from UI.ui_source_control import *
from ext import Watcher


class SourceControl(QWidget, Ui_SourceControl, Watcher):
    source_delete = pyqtSignal()
    source_modified = pyqtSignal()

    def __init__(self, index, glwindow, parent=None):
        super(SourceControl, self).__init__(parent)
        self.setupUi(self)

        # self.index = index                      # 当前控制器对应信号源序号
        self.glwindow = glwindow
        self.source = self.glwindow.sources[index]

        self.init_value()
        self.add_event()

    def init_value(self):
        self.freq_selector.setCurrentIndex(self.source.type)
        power = self.source.power
        power_w = pow(10, power / 10)
        self.power_slider.setValue(power)
        self.power_dbm.display(power)
        self.power_w.display(power_w)

        self.spin_x.setValue(self.source.position[0])
        self.spin_y.setValue(self.source.position[1])
        self.spin_z.setValue(self.source.position[2])

        self.show_check.setChecked(self.source.show)
        self.lock_check.setChecked(not self.source.enable)
        self.enable_all(self.source.enable)

    def add_event(self):
        self.show_check.stateChanged.connect(self.on_show_changed)
        self.lock_check.stateChanged.connect(self.on_lock_changed)
        self.focus_button.clicked.connect(self.focus)
        self.delete_button.clicked.connect(self.delete)
        self.freq_selector.activated[int].connect(self.on_freq_changed)
        self.power_slider.valueChanged[int].connect(self.on_power_changed)

        self.spin_x.valueChanged[float].connect(self.on_pos_x_changed)
        self.spin_y.valueChanged[float].connect(self.on_pos_y_changed)
        self.spin_z.valueChanged[float].connect(self.on_pos_z_changed)

    @Watcher.watch_modify
    def on_show_changed(self, state):
        if state == Qt.Checked:
            self.source.show = True
            self.lock_check.setChecked(False)   # 显示时默认解锁
        else:
            self.source.show = False
            self.lock_check.setChecked(True)    # 不显示时默认锁定
        self.glwindow.update()

    @Watcher.watch_modify
    def on_lock_changed(self, state):
        if state == Qt.Checked:
            self.source.enable = False
            self.enable_all(False)
        else:
            self.source.enable = True
            self.enable_all(True)

    def enable_all(self, enable):
        self.delete_button.setEnabled(enable)
        self.freq_selector.setEnabled(enable)
        self.power_slider.setEnabled(enable)
        self.spin_x.setEnabled(enable)
        self.spin_y.setEnabled(enable)
        self.spin_z.setEnabled(enable)

    def focus(self):
        self.glwindow.dx = -self.source.position[0]
        self.glwindow.dy = -self.source.position[1]
        self.glwindow.dz = -self.source.position[2]
        self.glwindow.update()

    @Watcher.watch_modify
    def delete(self, e):
        self.source_delete.emit()
        # self.glwindow.update()

    @Watcher.watch_modify
    def on_freq_changed(self, value):
        self.source.freq_change(value)
        self.glwindow.update()

    @Watcher.watch_modify
    def on_power_changed(self, value):
        self.source.power = value
        self.power_dbm.display(value)
        power = pow(10, value / 10)
        self.power_w.display(power)
        self.glwindow.update()

    # spin控制位置事件
    @Watcher.watch_modify
    def on_pos_x_changed(self, value):
        self.source.position[0] = value
        self.glwindow.update()

    @Watcher.watch_modify
    def on_pos_y_changed(self, value):
        self.source.position[1] = value
        self.glwindow.update()

    @Watcher.watch_modify
    def on_pos_z_changed(self, value):
        self.source.position[2] = value
        self.glwindow.update()

    def on_modified(self):
        self.source_modified.emit()

    def on_saved(self):
        self.modified = False
