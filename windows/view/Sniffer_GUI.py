# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Sniffer.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(850, 650)
        MainWindow.setAutoFillBackground(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.Uri_lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.Uri_lineEdit.setGeometry(QtCore.QRect(90, 60, 601, 31))
        self.Uri_lineEdit.setObjectName("Uri_lineEdit")
        self.Uri_label = QtWidgets.QLabel(self.centralwidget)
        self.Uri_label.setGeometry(QtCore.QRect(40, 66, 41, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Uri_label.setFont(font)
        self.Uri_label.setObjectName("Uri_label")
        self.Title_label = QtWidgets.QLabel(self.centralwidget)
        self.Title_label.setGeometry(QtCore.QRect(280, 20, 311, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.Title_label.setFont(font)
        self.Title_label.setObjectName("Title_label")
        self.Start_sniffer_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.Start_sniffer_pushButton.setGeometry(QtCore.QRect(710, 60, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Start_sniffer_pushButton.setFont(font)
        self.Start_sniffer_pushButton.setObjectName("Start_sniffer_pushButton")
        self.Sniffer_groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.Sniffer_groupBox.setGeometry(QtCore.QRect(30, 100, 781, 461))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Sniffer_groupBox.setFont(font)
        self.Sniffer_groupBox.setObjectName("Sniffer_groupBox")
        self.Sniffer_tableView = QtWidgets.QTableView(self.Sniffer_groupBox)
        self.Sniffer_tableView.setGeometry(QtCore.QRect(10, 30, 761, 421))
        self.Sniffer_tableView.setCornerButtonEnabled(False)
        self.Sniffer_tableView.setObjectName("Sniffer_tableView")
        self.Status_label = QtWidgets.QLabel(self.centralwidget)
        self.Status_label.setGeometry(QtCore.QRect(30, 570, 781, 16))
        self.Status_label.setObjectName("Status_label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 850, 26))
        self.menubar.setObjectName("menubar")
        self.Menu = QtWidgets.QMenu(self.menubar)
        self.Menu.setObjectName("Menu")
        MainWindow.setMenuBar(self.menubar)
        self.Statusbar = QtWidgets.QStatusBar(MainWindow)
        self.Statusbar.setObjectName("Statusbar")
        MainWindow.setStatusBar(self.Statusbar)
        self.Setting_action = QtWidgets.QAction(MainWindow)
        self.Setting_action.setObjectName("Setting_action")
        self.Exit_action = QtWidgets.QAction(MainWindow)
        self.Exit_action.setObjectName("Exit_action")
        self.Mode_action = QtWidgets.QAction(MainWindow)
        self.Mode_action.setObjectName("Mode_action")
        self.Menu.addAction(self.Mode_action)
        self.Menu.addAction(self.Setting_action)
        self.Menu.addAction(self.Exit_action)
        self.menubar.addAction(self.Menu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Stream video downloader"))
        self.Uri_label.setText(_translate("MainWindow", "Uri :"))
        self.Title_label.setText(_translate("MainWindow", "Stream video downloader"))
        self.Start_sniffer_pushButton.setText(_translate("MainWindow", "Start"))
        self.Sniffer_groupBox.setTitle(_translate("MainWindow", "Sniffer"))
        self.Status_label.setText(_translate("MainWindow", "Status"))
        self.Menu.setTitle(_translate("MainWindow", "Menu"))
        self.Setting_action.setText(_translate("MainWindow", "Settings"))
        self.Exit_action.setText(_translate("MainWindow", "Exit"))
        self.Mode_action.setText(_translate("MainWindow", "Mode"))
