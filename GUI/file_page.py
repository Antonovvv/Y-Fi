# -*- coding:utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
# import sys

from UI.ui_file_page import *
from GUI.building_control import BuildingControl
from GUI.source_control import SourceControl

from model import Building, Source
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
        self.building_count = 0
        self.source_count = 0

        self.init_value()
        self.add_event()

    def init_value(self):
        pass

    def add_event(self):
        self.glwindow.building_x_changed[float].connect(self.building_x_changed)
        self.glwindow.building_y_changed[float].connect(self.building_y_changed)
        self.glwindow.building_z_changed[float].connect(self.building_z_changed)

        self.glwindow.source_x_changed[float].connect(self.source_x_changed)
        self.glwindow.source_y_changed[float].connect(self.source_y_changed)
        self.glwindow.source_z_changed[float].connect(self.source_z_changed)

        self.highlight_check.stateChanged.connect(self.on_building_highlight)
        self.building_selector.activated[int].connect(self.on_building_selected)
        self.new_building_button.clicked.connect(self.new_building)

        self.source_selector.activated[int].connect(self.on_source_selected)
        self.new_source_button.clicked.connect(self.new_source)

    # 方向键控制building位置事件
    def building_x_changed(self, value):
        active = self.glwindow.active_building
        self.stackedBuilding.widget(active).spin_x.setValue(value)

    def building_y_changed(self, value):
        active = self.glwindow.active_building
        self.stackedBuilding.widget(active).spin_y.setValue(value)

    def building_z_changed(self, value):
        active = self.glwindow.active_building
        self.stackedBuilding.widget(active).spin_z.setValue(value)

    # 方向键控制信号源位置绑定spin值
    def source_x_changed(self, value):
        active = self.glwindow.active_source
        self.stackedSource.widget(active).spin_x.setValue(value)

    def source_y_changed(self, value):
        active = self.glwindow.active_source
        self.stackedSource.widget(active).spin_y.setValue(value)

    def source_z_changed(self, value):
        active = self.glwindow.active_source
        self.stackedSource.widget(active).spin_z.setValue(value)

    def on_building_highlight(self, state):
        if state == Qt.Checked:
            self.glwindow.HIGHLIGHT = True
        else:
            self.glwindow.HIGHLIGHT = False
        self.glwindow.update()

    def on_building_selected(self, value):
        self.stackedBuilding.setCurrentIndex(value)
        self.glwindow.active_building = value   # focus当前building
        self.glwindow.active_source = -1        # 移除对source的控制

    def on_source_selected(self, value):
        self.stackedSource.setCurrentIndex(value)
        self.glwindow.active_source = value     # focus当前source
        self.glwindow.active_building = -1      # 移除对building的控制

    def on_building_delete(self):
        index = self.stackedBuilding.currentIndex()

        self.glwindow.buildings.pop(index)
        self.stackedBuilding.removeWidget(self.stackedBuilding.widget(index))
        self.building_selector.removeItem(index)
        self.glwindow.active_building = self.stackedBuilding.currentIndex()

        self.glwindow.update()

    def on_source_delete(self):
        index = self.stackedSource.currentIndex()

        self.glwindow.sources.pop(index)
        self.stackedSource.removeWidget(self.stackedSource.widget(index))
        self.source_selector.removeItem(index)
        self.glwindow.active_source = self.stackedSource.currentIndex()

        self.glwindow.update()

    @Watcher.watch_modify
    def new_building(self, e):
        self.glwindow.buildings.append(Building())
        self.glwindow.update()

        index = self.stackedBuilding.count()
        new = BuildingControl(index, self.glwindow, self)
        self.stackedBuilding.addWidget(new)
        self.building_selector.addItem('build_' + str(self.building_count))
        self.building_count += 1

        self.building_selector.setCurrentIndex(index)
        self.stackedBuilding.setCurrentIndex(index)

        self.stackedBuilding.widget(index).building_delete.connect(self.on_building_delete)
        self.stackedBuilding.widget(index).building_modified.connect(self.on_modified)
        self.glwindow.active_building = index
        self.glwindow.active_source = -1

    @Watcher.watch_modify
    def new_source(self, e):
        self.glwindow.sources.append(Source())  # 新建信号源实例
        self.glwindow.update()

        index = self.stackedSource.count()
        new = SourceControl(index, self.glwindow, self)
        self.stackedSource.addWidget(new)
        self.source_selector.addItem('wifi_' + str(self.source_count))
        self.source_count += 1

        self.source_selector.setCurrentIndex(index)
        self.stackedSource.setCurrentIndex(index)

        self.stackedSource.widget(index).source_delete.connect(self.on_source_delete)   # 绑定事件
        self.stackedSource.widget(index).source_modified.connect(self.on_modified)
        self.glwindow.active_source = index
        self.glwindow.active_building = -1

    def open_init(self, buildings, sources):    # 打开文件后的初始化
        self.glwindow.buildings = buildings
        self.glwindow.sources = sources
        self.glwindow.active_building = 0
        self.glwindow.active_source = -1
        for index, building in enumerate(buildings):
            old = BuildingControl(index, self.glwindow, self)
            self.stackedBuilding.addWidget(old)
            self.building_selector.addItem('build_' + str(index))
            self.stackedBuilding.widget(index).building_delete.connect(self.on_building_delete)
            self.stackedBuilding.widget(index).building_modified.connect(self.on_modified)
        self.building_count = len(buildings)
        for index, source in enumerate(sources):
            old = SourceControl(index, self.glwindow, self)
            self.stackedSource.addWidget(old)
            self.source_selector.addItem('wifi_' + str(index))
            self.stackedSource.widget(index).source_delete.connect(self.on_source_delete)   # 绑定事件
            self.stackedSource.widget(index).source_modified.connect(self.on_modified)
        self.source_count = len(sources)

    def on_modified(self):
        self.file_modified.emit()

    def on_saved(self):
        self.modified = False
        for i in range(self.stackedSource.count()):
            self.stackedSource.widget(i).on_saved()

    def resizeEvent(self, e):
        self.model_view.resize(e.size().width()-360, e.size().height())
