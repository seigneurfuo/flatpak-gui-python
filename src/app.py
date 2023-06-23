#!/bin/env python3
import json
import sys
import os

from distutils import spawn

from flatpyk import Flatpyk

from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QHeaderView, QDesktopWidget
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt, QTranslator, QLocale

__name__ = "Flatpak GUI"
__version__ = "0.1.0"

FLATSEAL = "com.github.tchx84.Flatseal"

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.flatpyk_instance = Flatpyk()

        if not self.flatpyk_instance.flatpak_executable_found:
            print(self.tr("Unable to find the Flatpak executable in the path"))

        self.check_requirements()

        self.init_ui()
        self.init_events()

        self.refresh_data()

    def init_ui(self):
        loadUi(os.path.realpath(os.path.join(os.path.dirname(__file__), "mainwindow.ui")), self)

        self.setWindowTitle("{} {}".format(__name__,  __version__))

        self.tabWidget.setCurrentIndex(0)

    def init_events(self) -> None:
        self.refresh_action.triggered.connect(self.refresh_data)
        self.exit_action.triggered.connect(self.close)

        self.package_search.returnPressed.connect(self.on_search_text_changed)

        self.launch_button.clicked.connect(self.launch_flatpak)
        self.install_button.clicked.connect(self.install_flatpak)
        self.uninstall_button.clicked.connect(self.uninstall_flatpak)
        self.flatseal_install_button.clicked.connect(lambda install, FLATSEAL=FLATSEAL: self.flatpyk_instance.install([FLATSEAL]))
        self.flatseal_launch_button.clicked.connect(lambda run, FLATSEAL=FLATSEAL: self.flatpyk_instance.run(FLATSEAL))
        
        self.comboBox.currentIndexChanged.connect(self.refresh_data)

    def check_requirements(self) -> None:
        self.xterm_available = not spawn.find_executable("xterm")

    def refresh_data(self) -> None:
        installed_mode = self.comboBox.currentIndex() == 0
        self.launch_button.setEnabled(installed_mode)
        self.install_button.setEnabled(not installed_mode)
        self.uninstall_button.setEnabled(installed_mode)

        self.fill_flatpak_table()
        self.fill_runtimes_table()
        self.fill_remotes_table()
        self.fill_history_table()
        self.fill_tools_tab()

    def on_search_text_changed(self) -> None:
        self.fill_flatpak_table()
        self.fill_runtimes_table()

    def fill_flatpak_table(self) -> None:
        search = self.package_search.text()

        if self.comboBox.currentIndex() == 0:
            packages = self.flatpyk_instance.list_installed(filters=["apps"], search=search)
        else:
            packages = self.flatpyk_instance.list_availables(filters=["apps"], search=search, use_cached=True)
        
        self.tableWidget.setRowCount(len(packages))

        for row_index, row in enumerate(packages):
            for col_index, value in enumerate(row):
                item = QTableWidgetItem(value)
                
                if col_index == 0:
                    item.setData(Qt.UserRole, row[1])

                self.tableWidget.setItem(row_index, col_index, item)

        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.horizontalHeader().setSectionResizeMode(self.tableWidget.columnCount() - 1, QHeaderView.ResizeToContents)

    def fill_runtimes_table(self) -> None:
        search = self.package_search.text()

        if self.comboBox.currentIndex() == 0:
            runtimes = self.flatpyk_instance.list_installed(filters=["runtimes"], search=search)
            
        else:
            runtimes = self.flatpyk_instance.list_availables(filters=["runtimes"], search=search, use_cached=True)
        
        self.tableWidget_2.setRowCount(len(runtimes))

        for row_index, row in enumerate(runtimes):
            for col_index, value in enumerate(row):
                item = QTableWidgetItem(value)
                self.tableWidget_2.setItem(row_index, col_index, item)

        self.tableWidget_2.resizeColumnsToContents()
        self.tableWidget_2.horizontalHeader().setSectionResizeMode(self.tableWidget_2.columnCount() - 1, QHeaderView.ResizeToContents)

    def launch_flatpak(self) -> None:
        selected_item = self.tableWidget.item(self.tableWidget.currentRow(), 0)
        if selected_item:
            flatpak_id = selected_item.data(Qt.UserRole)
            self.flatpyk_instance.run(flatpak_id)

    def install_flatpak(self) -> None:
        selected_item = self.tableWidget.item(self.tableWidget.currentRow(), 0)
        if selected_item:
            flatpak_id = selected_item.data(Qt.UserRole)
            self.flatpyk_instance.install([flatpak_id])

            self.refresh_data()

    def uninstall_flatpak(self) -> None:
        selected_item = self.tableWidget.item(self.tableWidget.currentRow(), 0)
        if selected_item:
            flatpak_id = selected_item.data(Qt.UserRole)
            cmd = "flatpak uninstall {}".format(flatpak_id)
            self.flatpyk_instance.gui_terminal(cmd)

            self.refresh_data()

    def fill_remotes_table(self) -> None:
        remotes = self.flatpyk_instance.list_remotes()

        self.tableWidget_3.setRowCount(len(remotes))

        for row_index, row in enumerate(remotes):
            for col_index, value in enumerate(row):
                item = QTableWidgetItem(value)
                self.tableWidget_3.setItem(row_index, col_index, item)

        self.tableWidget_3.resizeColumnsToContents()
        self.tableWidget_3.horizontalHeader().setSectionResizeMode(self.tableWidget_3.columnCount() - 1, QHeaderView.ResizeToContents)

    def fill_history_table(self) -> None:
        history = self.flatpyk_instance.get_history()

        self.tableWidget_4.setRowCount(len(history))

        for row_index, row in enumerate(history):
            for col_index, value in enumerate(row):
                item = QTableWidgetItem(value)
                self.tableWidget_4.setItem(row_index, col_index, item)

        self.tableWidget_4.resizeColumnsToContents()
        self.tableWidget_4.horizontalHeader().setSectionResizeMode(self.tableWidget_3.columnCount() - 1, QHeaderView.ResizeToContents)

    def fill_tools_tab(self) -> None:
        # ----- Flatpak -----
        self.flatpak_checkbox.setChecked(self.flatpyk_instance.flatpak_executable_found)
        
        # ----- Flathub -----
        remotes = [remote[0] for remote in self.flatpyk_instance.list_remotes()]
        self.flathub_checkbox.setChecked("flathub" in remotes)

        # ----- Flatseal -----
        installed_apps = [package[1] for package in self.flatpyk_instance.list_installed(filters=["apps"])]

        if FLATSEAL in installed_apps:
            self.flatseal_install_button.setEnabled(False)
            self.flatseal_launch_button.setEnabled(True)
        else:
            self.flatseal_install_button.setEnabled(True)
            self.flatseal_launch_button.setEnabled(False)

def main() -> None:
    application = QApplication(sys.argv)

    translator = QTranslator(application)
    translator.load(QLocale().system().name(), os.path.join(os.path.dirname(os.path.realpath(__file__)), "translations"))
    application.installTranslator(translator)

    mainwindow = MainWindow()
    #mainwindow.move(QDesktopWidget().availableGeometry().center())
    mainwindow.show()

    sys.exit(application.exec())

main()