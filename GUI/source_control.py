# -*- coding:utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
# import sys

from UI.ui_source_control import *

from model import Source


class SourceControl(QWidget, Ui_SourceControl):
    source_delete = pyqtSignal()

    def __init__(self, index, glwindow, parent=None):
        super(SourceControl, self).__init__(parent)
        self.setupUi(self)

        # self.index = index                      # 当前控制器对应信号源序号
        self.glwindow = glwindow
        self.glwindow.sources.append(Source())  # 新建信号源实例
        self.glwindow.update()
        self.source = self.glwindow.sources[index]

        self.init_value()
        self.add_event()

    def init_value(self):
        power = self.source.power
        self.power_dbm.display(power)
        power_w = pow(10, power / 10)
        self.power_w.display(power_w)

        self.spin_x.setValue(self.source.position[0])
        self.spin_y.setValue(self.source.position[1])
        self.spin_z.setValue(self.source.position[2])

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

    def on_show_changed(self, state):
        if state == Qt.Checked:
            self.source.show = True
            self.lock_check.setChecked(False)   # 显示时默认解锁
        else:
            self.source.show = False
            self.lock_check.setChecked(True)    # 不显示时默认锁定
        self.glwindow.update()

    def on_lock_changed(self, state):
        if state == Qt.Checked:
            self.source.enable = False
            self.switch_all(False)
        else:
            self.source.enable = True
            self.switch_all(True)

    def switch_all(self, enable):
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

    def delete(self):
        self.source_delete.emit()
        # self.glwindow.update()

    def on_freq_changed(self, value):
        self.source.freq_change(value)
        self.glwindow.update()

    def on_power_changed(self, value):
        self.source.power = value
        self.power_dbm.display(value)
        power = pow(10, value / 10)
        self.power_w.display(power)
        self.glwindow.update()

    # spin控制位置事件
    def on_pos_x_changed(self, value):
        self.source.position[0] = value
        self.glwindow.update()

    def on_pos_y_changed(self, value):
        self.source.position[1] = value
        self.glwindow.update()

    def on_pos_z_changed(self, value):
        self.source.position[2] = value
        self.glwindow.update()
