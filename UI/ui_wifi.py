# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_wifi.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_WifiBox(object):
    def setupUi(self, WifiBox):
        WifiBox.setObjectName("WifiBox")
        WifiBox.resize(335, 265)
        self.groupBox = QtWidgets.QGroupBox(WifiBox)
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

        self.retranslateUi(WifiBox)
        QtCore.QMetaObject.connectSlotsByName(WifiBox)

    def retranslateUi(self, WifiBox):
        _translate = QtCore.QCoreApplication.translate
        WifiBox.setWindowTitle(_translate("WifiBox", "Form"))
        self.groupBox.setTitle(_translate("WifiBox", "wifi参数"))
        self.label_5.setText(_translate("WifiBox", "y坐标"))
        self.label_2.setText(_translate("WifiBox", "发射功率(dBm)"))
        self.label_6.setText(_translate("WifiBox", "z坐标"))
        self.label_4.setText(_translate("WifiBox", "x坐标"))
        self.label.setText(_translate("WifiBox", "发射频段"))
        self.label_3.setText(_translate("WifiBox", "位置"))
