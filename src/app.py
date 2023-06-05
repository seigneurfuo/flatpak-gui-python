#!/bin/env python3
import json
import sys
import os
from pathlib import Path

from flatpyk import Flatpyk

from PyQt5.QtGui import QColor, QDesktopServices
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QHeaderView
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt, QUrl

__name__ = "Flatpak GUI"
__version__ = "0.1.0"

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.flatpyk_instance = Flatpyk()

        self.init_ui()
        self.init_events()

        self.refresh_data()

    def init_ui(self):
        loadUi(os.path.realpath(os.path.join(os.path.dirname(__file__), "mainwindow.ui")), self)

        self.setWindowTitle("{} {}".format(__name__,  __version__))

        self.tabWidget.setCurrentIndex(0)

    def init_events(self):
         self.refresh_action.triggered.connect(self.refresh_data)

    def refresh_data():
        self.fill_flatpak_table()
        self.fill_runtimes_table()

    def fill_flatpak_table(self):
        installed_packages = self.flatpyk_instance.list_installed(filters=["apps"])
        
        self.tableWidget.setRowCount(len(installed_packages))

        for row_index, row in enumerate(installed_packages):
            for col_index, value in enumerate(row):
                item = QTableWidgetItem(value)
                self.tableWidget.setItem(row_index, col_index, item)

        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.horizontalHeader().setSectionResizeMode(self.tableWidget.columnCount() - 1, QHeaderView.ResizeToContents)

    def fill_runtimes_table(self):
        installed_runtimes = self.flatpyk_instance.list_installed(filters=["runtimes"])
        
        self.tableWidget_2.setRowCount(len(installed_runtimes))

        for row_index, row in enumerate(installed_runtimes):
            for col_index, value in enumerate(row):
                item = QTableWidgetItem(value)
                self.tableWidget_2.setItem(row_index, col_index, item)

        self.tableWidget_2.resizeColumnsToContents()
        self.tableWidget_2.horizontalHeader().setSectionResizeMode(self.tableWidget_2.columnCount() - 1, QHeaderView.ResizeToContents)


def main():
    import cgitb
    cgitb.enable(format='text')

    application = QApplication(sys.argv)
    mainwindow = MainWindow()
    mainwindow.move(application.desktop().screen().rect().center() - mainwindow.rect().center())
    mainwindow.show()
    application.exec()

main()