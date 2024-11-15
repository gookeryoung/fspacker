# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'CNMapViewer.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.action_New = QAction(MainWindow)
        self.action_New.setObjectName("action_New")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName("menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 22))
        self.menu_File = QMenu(self.menubar)
        self.menu_File.setObjectName("menu_File")
        self.menu_Edit = QMenu(self.menubar)
        self.menu_Edit.setObjectName("menu_Edit")
        self.menu_About = QMenu(self.menubar)
        self.menu_About.setObjectName("menu_About")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menu_File.menuAction())
        self.menubar.addAction(self.menu_Edit.menuAction())
        self.menubar.addAction(self.menu_About.menuAction())
        self.menu_File.addAction(self.action_New)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", "MainWindow", None))
        self.action_New.setText(QCoreApplication.translate("MainWindow", "&New", None))
        self.menu_File.setTitle(QCoreApplication.translate("MainWindow", "&File", None))
        self.menu_Edit.setTitle(QCoreApplication.translate("MainWindow", "&Edit", None))
        self.menu_About.setTitle(QCoreApplication.translate("MainWindow", "&About", None))

    # retranslateUi
