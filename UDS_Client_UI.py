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
        MainWindow.resize(725, 517)
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
        self.tabWidget.setGeometry(QtCore.QRect(0, 150, 721, 321))
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
        self.textEdit_trace = QtWidgets.QTextEdit(self.CANUDS)
        self.textEdit_trace.setGeometry(QtCore.QRect(0, 100, 391, 191))
        self.textEdit_trace.setObjectName("textEdit_trace")
        self.lineEdit_send = QtWidgets.QLineEdit(self.CANUDS)
        self.lineEdit_send.setGeometry(QtCore.QRect(0, 0, 711, 20))
        self.lineEdit_send.setObjectName("lineEdit_send")
        self.pushButton_send = QtWidgets.QPushButton(self.CANUDS)
        self.pushButton_send.setEnabled(False)
        self.pushButton_send.setGeometry(QtCore.QRect(640, 30, 75, 23))
        self.pushButton_send.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.pushButton_send.setCheckable(False)
        self.pushButton_send.setAutoDefault(False)
        self.pushButton_send.setFlat(False)
        self.pushButton_send.setObjectName("pushButton_send")
        self.checkBox_3E = QtWidgets.QCheckBox(self.CANUDS)
        self.checkBox_3E.setEnabled(False)
        self.checkBox_3E.setGeometry(QtCore.QRect(0, 30, 111, 23))
        self.checkBox_3E.setObjectName("checkBox_3E")
        self.checkBox_sendcanfd = QtWidgets.QCheckBox(self.CANUDS)
        self.checkBox_sendcanfd.setEnabled(True)
        self.checkBox_sendcanfd.setGeometry(QtCore.QRect(560, 30, 68, 23))
        self.checkBox_sendcanfd.setObjectName("checkBox_sendcanfd")
        self.listView_dids = QtWidgets.QListView(self.CANUDS)
        self.listView_dids.setGeometry(QtCore.QRect(565, 60, 141, 231))
        self.listView_dids.setObjectName("listView_dids")
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
        self.comboBox_channel = QtWidgets.QComboBox(self.groupBox)
        self.comboBox_channel.setGeometry(QtCore.QRect(53, 15, 251, 19))
        self.comboBox_channel.setObjectName("comboBox_channel")
        self.label_channel = QtWidgets.QLabel(self.groupBox)
        self.label_channel.setGeometry(QtCore.QRect(10, 10, 51, 29))
        self.label_channel.setObjectName("label_channel")
        self.checkBox_bustype = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_bustype.setGeometry(QtCore.QRect(10, 40, 81, 23))
        self.checkBox_bustype.setObjectName("checkBox_bustype")
        self.pushButton_start = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_start.setGeometry(QtCore.QRect(450, 10, 61, 23))
        self.pushButton_start.setObjectName("pushButton_start")
        self.horizontalLayoutWidget_3 = QtWidgets.QWidget(self.groupBox)
        self.horizontalLayoutWidget_3.setGeometry(QtCore.QRect(310, 40, 121, 21))
        self.horizontalLayoutWidget_3.setObjectName("horizontalLayoutWidget_3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_3)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_channel_3 = QtWidgets.QLabel(self.horizontalLayoutWidget_3)
        self.label_channel_3.setObjectName("label_channel_3")
        self.horizontalLayout_3.addWidget(self.label_channel_3)
        self.lineEdit_requestid = QtWidgets.QLineEdit(self.horizontalLayoutWidget_3)
        self.lineEdit_requestid.setObjectName("lineEdit_requestid")
        self.horizontalLayout_3.addWidget(self.lineEdit_requestid)
        self.horizontalLayoutWidget_4 = QtWidgets.QWidget(self.groupBox)
        self.horizontalLayoutWidget_4.setGeometry(QtCore.QRect(310, 70, 121, 21))
        self.horizontalLayoutWidget_4.setObjectName("horizontalLayoutWidget_4")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_4)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_channel_4 = QtWidgets.QLabel(self.horizontalLayoutWidget_4)
        self.label_channel_4.setObjectName("label_channel_4")
        self.horizontalLayout_4.addWidget(self.label_channel_4)
        self.lineEdit_responseid = QtWidgets.QLineEdit(self.horizontalLayoutWidget_4)
        self.lineEdit_responseid.setObjectName("lineEdit_responseid")
        self.horizontalLayout_4.addWidget(self.lineEdit_responseid)
        self.horizontalLayoutWidget_5 = QtWidgets.QWidget(self.groupBox)
        self.horizontalLayoutWidget_5.setGeometry(QtCore.QRect(310, 100, 121, 21))
        self.horizontalLayoutWidget_5.setObjectName("horizontalLayoutWidget_5")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_5)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_channel_5 = QtWidgets.QLabel(self.horizontalLayoutWidget_5)
        self.label_channel_5.setObjectName("label_channel_5")
        self.horizontalLayout_5.addWidget(self.label_channel_5)
        self.lineEdit_functionid = QtWidgets.QLineEdit(self.horizontalLayoutWidget_5)
        self.lineEdit_functionid.setObjectName("lineEdit_functionid")
        self.horizontalLayout_5.addWidget(self.lineEdit_functionid)
        self.comboBox_eculist = QtWidgets.QComboBox(self.groupBox)
        self.comboBox_eculist.setGeometry(QtCore.QRect(339, 10, 91, 22))
        self.comboBox_eculist.setObjectName("comboBox_eculist")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(310, 10, 31, 19))
        self.label.setObjectName("label")
        self.textBrowser = QtWidgets.QTextBrowser(self.groupBox)
        self.textBrowser.setGeometry(QtCore.QRect(520, 10, 191, 121))
        self.textBrowser.setObjectName("textBrowser")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 725, 22))
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
        self.label_channel.setText(_translate("MainWindow", "Channel"))
        self.checkBox_bustype.setText(_translate("MainWindow", "CANFD BUS"))
        self.pushButton_start.setText(_translate("MainWindow", "Start"))
        self.label_channel_3.setText(_translate("MainWindow", "ReqID"))
        self.lineEdit_requestid.setText(_translate("MainWindow", "0x123"))
        self.label_channel_4.setText(_translate("MainWindow", "ResID"))
        self.lineEdit_responseid.setText(_translate("MainWindow", "0x234"))
        self.label_channel_5.setText(_translate("MainWindow", "FunID"))
        self.lineEdit_functionid.setText(_translate("MainWindow", "0x345"))
        self.label.setText(_translate("MainWindow", "ECU:"))
        self.menu.setTitle(_translate("MainWindow", "关于"))
