# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UDS_Client_UI.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(723, 467)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        MainWindow.setPalette(palette)
        MainWindow.setTabletTracking(False)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setDocumentMode(False)
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setEnabled(True)
        self.tabWidget.setGeometry(QtCore.QRect(0, 150, 721, 271))
        self.tabWidget.setAutoFillBackground(False)
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.South)
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabWidget.setIconSize(QtCore.QSize(16, 16))
        self.tabWidget.setElideMode(QtCore.Qt.ElideLeft)
        self.tabWidget.setUsesScrollButtons(True)
        self.tabWidget.setDocumentMode(False)
        self.tabWidget.setTabsClosable(False)
        self.tabWidget.setMovable(False)
        self.tabWidget.setTabBarAutoHide(False)
        self.tabWidget.setObjectName("tabWidget")
        self.CANUDS = QtWidgets.QWidget()
        self.CANUDS.setObjectName("CANUDS")
        self.textEdit = QtWidgets.QTextEdit(self.CANUDS)
        self.textEdit.setGeometry(QtCore.QRect(0, 100, 711, 141))
        self.textEdit.setObjectName("textEdit")
        self.lineEdit = QtWidgets.QLineEdit(self.CANUDS)
        self.lineEdit.setGeometry(QtCore.QRect(0, 0, 711, 20))
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton_send = QtWidgets.QPushButton(self.CANUDS)
        self.pushButton_send.setEnabled(False)
        self.pushButton_send.setGeometry(QtCore.QRect(640, 30, 75, 23))
        self.pushButton_send.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.pushButton_send.setCheckable(False)
        self.pushButton_send.setAutoDefault(False)
        self.pushButton_send.setFlat(False)
        self.pushButton_send.setObjectName("pushButton_send")
        self.checkBox_3E = QtWidgets.QCheckBox(self.CANUDS)
        self.checkBox_3E.setGeometry(QtCore.QRect(0, 30, 111, 23))
        self.checkBox_3E.setObjectName("checkBox_3E")
        self.checkBox_sendcanfd = QtWidgets.QCheckBox(self.CANUDS)
        self.checkBox_sendcanfd.setGeometry(QtCore.QRect(560, 30, 68, 23))
        self.checkBox_sendcanfd.setObjectName("checkBox_sendcanfd")
        self.tabWidget.addTab(self.CANUDS, "")
        self.CANFlash = QtWidgets.QWidget()
        self.CANFlash.setObjectName("CANFlash")
        self.tabWidget.addTab(self.CANFlash, "")
        self.DoIPUDS = QtWidgets.QWidget()
        self.DoIPUDS.setObjectName("DoIPUDS")
        self.tabWidget.addTab(self.DoIPUDS, "")
        self.DoIPFlash = QtWidgets.QWidget()
        self.DoIPFlash.setObjectName("DoIPFlash")
        self.tabWidget.addTab(self.DoIPFlash, "")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(0, 0, 721, 141))
        self.groupBox.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.groupBox)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(10, 50, 221, 21))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_channel_2 = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        self.label_channel_2.setObjectName("label_channel_2")
        self.horizontalLayout_2.addWidget(self.label_channel_2)
        self.lineEdit_channel_2 = QtWidgets.QLineEdit(self.horizontalLayoutWidget_2)
        self.lineEdit_channel_2.setObjectName("lineEdit_channel_2")
        self.horizontalLayout_2.addWidget(self.lineEdit_channel_2)
        self.comboBox_channel = QtWidgets.QComboBox(self.groupBox)
        self.comboBox_channel.setGeometry(QtCore.QRect(50, 20, 251, 19))
        self.comboBox_channel.setObjectName("comboBox_channel")
        self.label_channel = QtWidgets.QLabel(self.groupBox)
        self.label_channel.setGeometry(QtCore.QRect(7, 15, 51, 29))
        self.label_channel.setObjectName("label_channel")
        self.checkBox_bustype = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_bustype.setGeometry(QtCore.QRect(10, 80, 81, 23))
        self.checkBox_bustype.setObjectName("checkBox_bustype")
        self.pushButton_start = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_start.setGeometry(QtCore.QRect(340, 20, 61, 23))
        self.pushButton_start.setObjectName("pushButton_start")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 723, 22))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton_send.setText(_translate("MainWindow", "send"))
        self.checkBox_3E.setText(_translate("MainWindow", "Tester Preaent"))
        self.checkBox_sendcanfd.setText(_translate("MainWindow", "CANFD"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.CANUDS), _translate("MainWindow", "CAN UDS"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.CANFlash), _translate("MainWindow", "CAN Flash"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.DoIPUDS), _translate("MainWindow", "DoIP UDS"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.DoIPFlash), _translate("MainWindow", "DoIP Flash"))
        self.label_channel_2.setText(_translate("MainWindow", "Channel"))
        self.label_channel.setText(_translate("MainWindow", "Channel"))
        self.checkBox_bustype.setText(_translate("MainWindow", "CANFD BUS"))
        self.pushButton_start.setText(_translate("MainWindow", "Start"))
        self.menu.setTitle(_translate("MainWindow", "关于"))
