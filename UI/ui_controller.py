# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_controller.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(1171, 655)
        MainWindow.setMinimumSize(QtCore.QSize(360, 640))
        MainWindow.setMaximumSize(QtCore.QSize(3000, 3000))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setEnabled(True)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 360, 600))
        self.tabWidget.setMinimumSize(QtCore.QSize(360, 600))
        self.tabWidget.setMaximumSize(QtCore.QSize(360, 600))
        self.tabWidget.setObjectName("tabWidget")
        self.model_page = QtWidgets.QWidget()
        self.model_page.setObjectName("model_page")
        self.floor_box = QtWidgets.QGroupBox(self.model_page)
        self.floor_box.setGeometry(QtCore.QRect(20, 10, 311, 201))
        self.floor_box.setObjectName("floor_box")
        self.gridLayoutWidget = QtWidgets.QWidget(self.floor_box)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(30, 30, 251, 151))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label_floor_thickness = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_floor_thickness.setObjectName("label_floor_thickness")
        self.gridLayout.addWidget(self.label_floor_thickness, 2, 0, 1, 1)
        self.label_floors = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_floors.setObjectName("label_floors")
        self.gridLayout.addWidget(self.label_floors, 0, 0, 1, 1)
        self.label_rooms = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_rooms.setObjectName("label_rooms")
        self.gridLayout.addWidget(self.label_rooms, 1, 0, 1, 1)
        self.spin_rooms = QtWidgets.QSpinBox(self.gridLayoutWidget)
        self.spin_rooms.setMinimum(1)
        self.spin_rooms.setMaximum(20)
        self.spin_rooms.setObjectName("spin_rooms")
        self.gridLayout.addWidget(self.spin_rooms, 1, 1, 1, 1)
        self.spin_floors = QtWidgets.QSpinBox(self.gridLayoutWidget)
        self.spin_floors.setAccelerated(False)
        self.spin_floors.setMinimum(1)
        self.spin_floors.setObjectName("spin_floors")
        self.gridLayout.addWidget(self.spin_floors, 0, 1, 1, 1)
        self.spin_floor_thickness = QtWidgets.QDoubleSpinBox(self.gridLayoutWidget)
        self.spin_floor_thickness.setMinimum(0.1)
        self.spin_floor_thickness.setMaximum(2.0)
        self.spin_floor_thickness.setSingleStep(0.05)
        self.spin_floor_thickness.setProperty("value", 0.3)
        self.spin_floor_thickness.setObjectName("spin_floor_thickness")
        self.gridLayout.addWidget(self.spin_floor_thickness, 2, 1, 1, 1)
        self.room_box = QtWidgets.QGroupBox(self.model_page)
        self.room_box.setGeometry(QtCore.QRect(20, 230, 311, 241))
        self.room_box.setObjectName("room_box")
        self.gridLayoutWidget_2 = QtWidgets.QWidget(self.room_box)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(30, 30, 251, 191))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_2.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_room_width = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.label_room_width.setObjectName("label_room_width")
        self.gridLayout_2.addWidget(self.label_room_width, 3, 0, 1, 1)
        self.label_room_height = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.label_room_height.setObjectName("label_room_height")
        self.gridLayout_2.addWidget(self.label_room_height, 4, 0, 1, 1)
        self.spin_room_length = QtWidgets.QDoubleSpinBox(self.gridLayoutWidget_2)
        self.spin_room_length.setDecimals(1)
        self.spin_room_length.setMinimum(2.0)
        self.spin_room_length.setMaximum(50.0)
        self.spin_room_length.setSingleStep(0.2)
        self.spin_room_length.setProperty("value", 10.0)
        self.spin_room_length.setObjectName("spin_room_length")
        self.gridLayout_2.addWidget(self.spin_room_length, 1, 1, 1, 1)
        self.spin_room_width = QtWidgets.QDoubleSpinBox(self.gridLayoutWidget_2)
        self.spin_room_width.setDecimals(1)
        self.spin_room_width.setMinimum(2.0)
        self.spin_room_width.setMaximum(50.0)
        self.spin_room_width.setSingleStep(0.2)
        self.spin_room_width.setProperty("value", 5.0)
        self.spin_room_width.setObjectName("spin_room_width")
        self.gridLayout_2.addWidget(self.spin_room_width, 3, 1, 1, 1)
        self.spin_room_height = QtWidgets.QDoubleSpinBox(self.gridLayoutWidget_2)
        self.spin_room_height.setDecimals(1)
        self.spin_room_height.setMinimum(2.0)
        self.spin_room_height.setMaximum(50.0)
        self.spin_room_height.setSingleStep(0.2)
        self.spin_room_height.setProperty("value", 5.0)
        self.spin_room_height.setObjectName("spin_room_height")
        self.gridLayout_2.addWidget(self.spin_room_height, 4, 1, 1, 1)
        self.label_room_length = QtWidgets.QLabel(self.gridLayoutWidget_2)
        font = QtGui.QFont()
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        font.setKerning(True)
        font.setStyleStrategy(QtGui.QFont.PreferDefault)
        self.label_room_length.setFont(font)
        self.label_room_length.setWordWrap(False)
        self.label_room_length.setObjectName("label_room_length")
        self.gridLayout_2.addWidget(self.label_room_length, 1, 0, 1, 1)
        self.label_wall_thickness = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.label_wall_thickness.setObjectName("label_wall_thickness")
        self.gridLayout_2.addWidget(self.label_wall_thickness, 5, 0, 1, 1)
        self.spin_wall_thickness = QtWidgets.QDoubleSpinBox(self.gridLayoutWidget_2)
        self.spin_wall_thickness.setMinimum(0.05)
        self.spin_wall_thickness.setMaximum(2.0)
        self.spin_wall_thickness.setSingleStep(0.05)
        self.spin_wall_thickness.setProperty("value", 0.1)
        self.spin_wall_thickness.setObjectName("spin_wall_thickness")
        self.gridLayout_2.addWidget(self.spin_wall_thickness, 5, 1, 1, 1)
        self.tabWidget.addTab(self.model_page, "")
        self.sources_page = QtWidgets.QWidget()
        self.sources_page.setObjectName("sources_page")
        self.source_selector = QtWidgets.QComboBox(self.sources_page)
        self.source_selector.setGeometry(QtCore.QRect(90, 20, 171, 21))
        self.source_selector.setObjectName("source_selector")
        self.source_selector.addItem("")
        self.stackedWidget = QtWidgets.QStackedWidget(self.sources_page)
        self.stackedWidget.setGeometry(QtCore.QRect(10, 60, 331, 311))
        self.stackedWidget.setObjectName("stackedWidget")
        self.page_new = QtWidgets.QWidget()
        self.page_new.setObjectName("page_new")
        self.stackedWidget.addWidget(self.page_new)
        self.page_use = QtWidgets.QWidget()
        self.page_use.setObjectName("page_use")
        self.groupBox = QtWidgets.QGroupBox(self.page_use)
        self.groupBox.setGeometry(QtCore.QRect(0, 0, 331, 261))
        self.groupBox.setObjectName("groupBox")
        self.gridLayoutWidget_3 = QtWidgets.QWidget(self.groupBox)
        self.gridLayoutWidget_3.setGeometry(QtCore.QRect(10, 20, 311, 131))
        self.gridLayoutWidget_3.setObjectName("gridLayoutWidget_3")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.gridLayoutWidget_3)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.comboBox_2 = QtWidgets.QComboBox(self.gridLayoutWidget_3)
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.gridLayout_3.addWidget(self.comboBox_2, 0, 2, 1, 2)
        self.label_5 = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.label_5.setObjectName("label_5")
        self.gridLayout_3.addWidget(self.label_5, 2, 2, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.label_2.setObjectName("label_2")
        self.gridLayout_3.addWidget(self.label_2, 1, 0, 1, 2)
        self.doubleSpinBox_3 = QtWidgets.QDoubleSpinBox(self.gridLayoutWidget_3)
        self.doubleSpinBox_3.setObjectName("doubleSpinBox_3")
        self.gridLayout_3.addWidget(self.doubleSpinBox_3, 3, 3, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.label_6.setObjectName("label_6")
        self.gridLayout_3.addWidget(self.label_6, 2, 3, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.label_4.setObjectName("label_4")
        self.gridLayout_3.addWidget(self.label_4, 2, 1, 1, 1)
        self.doubleSpinBox = QtWidgets.QDoubleSpinBox(self.gridLayoutWidget_3)
        self.doubleSpinBox.setObjectName("doubleSpinBox")
        self.gridLayout_3.addWidget(self.doubleSpinBox, 3, 1, 1, 1)
        self.doubleSpinBox_2 = QtWidgets.QDoubleSpinBox(self.gridLayoutWidget_3)
        self.doubleSpinBox_2.setObjectName("doubleSpinBox_2")
        self.gridLayout_3.addWidget(self.doubleSpinBox_2, 3, 2, 1, 1)
        self.label = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.label.setObjectName("label")
        self.gridLayout_3.addWidget(self.label, 0, 0, 1, 2)
        self.horizontalSlider = QtWidgets.QSlider(self.gridLayoutWidget_3)
        self.horizontalSlider.setMinimum(10)
        self.horizontalSlider.setMaximum(20)
        self.horizontalSlider.setProperty("value", 15)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.horizontalSlider.setTickInterval(1)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.gridLayout_3.addWidget(self.horizontalSlider, 1, 2, 1, 2)
        self.label_3 = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.label_3.setObjectName("label_3")
        self.gridLayout_3.addWidget(self.label_3, 2, 0, 2, 1)
        self.button_new_source = QtWidgets.QPushButton(self.groupBox)
        self.button_new_source.setGeometry(QtCore.QRect(140, 180, 56, 21))
        self.button_new_source.setObjectName("button_new_source")
        self.stackedWidget.addWidget(self.page_use)
        self.tabWidget.addTab(self.sources_page, "")
        self.model_view = QtWidgets.QStackedWidget(self.centralwidget)
        self.model_view.setGeometry(QtCore.QRect(359, 9, 801, 591))
        self.model_view.setObjectName("model_view")
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")
        self.model_view.addWidget(self.page)
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.model_view.addWidget(self.page_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1171, 18))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.new_file = QtWidgets.QAction(MainWindow)
        self.new_file.setObjectName("new_file")
        self.open_file = QtWidgets.QAction(MainWindow)
        self.open_file.setObjectName("open_file")
        self.save_file = QtWidgets.QAction(MainWindow)
        self.save_file.setObjectName("save_file")
        self.menu.addAction(self.new_file)
        self.menu.addAction(self.open_file)
        self.menu.addAction(self.save_file)
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(1)
        self.source_selector.setCurrentIndex(0)
        self.stackedWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Controller"))
        self.floor_box.setTitle(_translate("MainWindow", "楼层参数"))
        self.label_floor_thickness.setText(_translate("MainWindow", "层间厚度"))
        self.label_floors.setText(_translate("MainWindow", "层数"))
        self.label_rooms.setText(_translate("MainWindow", "每层房间数"))
        self.room_box.setTitle(_translate("MainWindow", "房间参数"))
        self.label_room_width.setText(_translate("MainWindow", "房间宽度"))
        self.label_room_height.setText(_translate("MainWindow", "房间高度"))
        self.label_room_length.setText(_translate("MainWindow", "房间长度    "))
        self.label_wall_thickness.setText(_translate("MainWindow", "墙厚度"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.model_page), _translate("MainWindow", "Model"))
        self.source_selector.setCurrentText(_translate("MainWindow", "new source"))
        self.source_selector.setItemText(0, _translate("MainWindow", "new source"))
        self.groupBox.setTitle(_translate("MainWindow", "wifi参数"))
        self.comboBox_2.setItemText(0, _translate("MainWindow", "5.0GHz"))
        self.comboBox_2.setItemText(1, _translate("MainWindow", "2.4GHz"))
        self.label_5.setText(_translate("MainWindow", "y坐标"))
        self.label_2.setText(_translate("MainWindow", "发射功率(dBm)"))
        self.label_6.setText(_translate("MainWindow", "z坐标"))
        self.label_4.setText(_translate("MainWindow", "x坐标"))
        self.label.setText(_translate("MainWindow", "发射频段"))
        self.label_3.setText(_translate("MainWindow", "位置"))
        self.button_new_source.setText(_translate("MainWindow", "new"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.sources_page), _translate("MainWindow", "Sources"))
        self.menu.setTitle(_translate("MainWindow", "File"))
        self.new_file.setText(_translate("MainWindow", "New"))
        self.open_file.setText(_translate("MainWindow", "Open"))
        self.save_file.setText(_translate("MainWindow", "Save"))
