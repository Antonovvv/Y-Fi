# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_file_page.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_FilePage(object):
    def setupUi(self, FilePage):
        FilePage.setObjectName("FilePage")
        FilePage.resize(1000, 701)
        FilePage.setMinimumSize(QtCore.QSize(1000, 0))
        self.tabWidget = QtWidgets.QTabWidget(FilePage)
        self.tabWidget.setEnabled(True)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 360, 681))
        self.tabWidget.setMinimumSize(QtCore.QSize(360, 600))
        self.tabWidget.setMaximumSize(QtCore.QSize(360, 800))
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.West)
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Triangular)
        self.tabWidget.setElideMode(QtCore.Qt.ElideNone)
        self.tabWidget.setUsesScrollButtons(True)
        self.tabWidget.setDocumentMode(False)
        self.tabWidget.setTabsClosable(False)
        self.tabWidget.setMovable(False)
        self.tabWidget.setTabBarAutoHide(False)
        self.tabWidget.setObjectName("tabWidget")
        self.building_page = QtWidgets.QWidget()
        self.building_page.setObjectName("building_page")
        self.building_selector = QtWidgets.QComboBox(self.building_page)
        self.building_selector.setGeometry(QtCore.QRect(20, 20, 141, 31))
        self.building_selector.setCurrentText("")
        self.building_selector.setObjectName("building_selector")
        self.new_building_button = QtWidgets.QPushButton(self.building_page)
        self.new_building_button.setGeometry(QtCore.QRect(210, 10, 56, 31))
        self.new_building_button.setObjectName("new_building_button")
        self.stackedBuilding = QtWidgets.QStackedWidget(self.building_page)
        self.stackedBuilding.setGeometry(QtCore.QRect(0, 80, 341, 600))
        self.stackedBuilding.setMinimumSize(QtCore.QSize(0, 600))
        self.stackedBuilding.setObjectName("stackedBuilding")
        self.highlight_check = QtWidgets.QCheckBox(self.building_page)
        self.highlight_check.setGeometry(QtCore.QRect(210, 50, 91, 19))
        self.highlight_check.setChecked(True)
        self.highlight_check.setObjectName("highlight_check")
        self.tabWidget.addTab(self.building_page, "")
        self.sources_page = QtWidgets.QWidget()
        self.sources_page.setObjectName("sources_page")
        self.source_selector = QtWidgets.QComboBox(self.sources_page)
        self.source_selector.setGeometry(QtCore.QRect(50, 20, 141, 31))
        self.source_selector.setCurrentText("")
        self.source_selector.setObjectName("source_selector")
        self.stackedSource = QtWidgets.QStackedWidget(self.sources_page)
        self.stackedSource.setGeometry(QtCore.QRect(0, 60, 341, 501))
        self.stackedSource.setObjectName("stackedSource")
        self.new_source_button = QtWidgets.QPushButton(self.sources_page)
        self.new_source_button.setGeometry(QtCore.QRect(240, 20, 56, 31))
        self.new_source_button.setObjectName("new_source_button")
        self.tabWidget.addTab(self.sources_page, "")
        self.model_view = QtWidgets.QStackedWidget(FilePage)
        self.model_view.setGeometry(QtCore.QRect(360, 0, 801, 591))
        self.model_view.setMinimumSize(QtCore.QSize(640, 500))
        self.model_view.setObjectName("model_view")

        self.retranslateUi(FilePage)
        self.tabWidget.setCurrentIndex(0)
        self.building_selector.setCurrentIndex(-1)
        self.stackedBuilding.setCurrentIndex(-1)
        self.source_selector.setCurrentIndex(-1)
        self.stackedSource.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(FilePage)

    def retranslateUi(self, FilePage):
        _translate = QtCore.QCoreApplication.translate
        FilePage.setWindowTitle(_translate("FilePage", "Form"))
        self.new_building_button.setText(_translate("FilePage", "new"))
        self.highlight_check.setText(_translate("FilePage", "高亮"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.building_page), _translate("FilePage", "Buildings"))
        self.new_source_button.setText(_translate("FilePage", "new"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.sources_page), _translate("FilePage", "Sources"))
