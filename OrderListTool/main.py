# main window
import sys
import os
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QStatusBar,
    QHBoxLayout,
    QVBoxLayout,
    QScrollArea,
    QLabel,
    QPushButton,
    QCheckBox,
    QComboBox,
    QFileDialog,
    QMessageBox
)
# from PyQt5.QtGui import *
from PyQt5.QtCore import Qt, QCoreApplication

import settings as Settings
import definitions as Definitions
import dispatcher as Dispatcher
import visualization as Visualization
import language as Lang

class MainWindow(QMainWindow):
    dispatcher = 0

    def __init__(self):
        super().__init__()
        # window settings
        self.window_settings = {"view_grouped":True}
        # create instances
        self.dispatcher = Dispatcher.Dispatcher()
        self.visualization = Visualization.Visualization(self.dispatcher,self.window_settings)
        # get default values
        self.file_name_bom = self.dispatcher.get_cad_system().get_default_file()
        self.path_database = self.dispatcher.get_cad_system().get_default_directory()
        # buil UI
        self.init_ui()

    def init_ui(self):
        # boxes
        self.box_window = QVBoxLayout()
        self.box_header = QVBoxLayout()
        self.box_header_bom = QHBoxLayout()
        self.box_header_database = QHBoxLayout()
        self.box_commands = QHBoxLayout()
        self.scroll_body = QScrollArea()
        self.scroll_widget = QWidget()
        self.box_body = QVBoxLayout()
        self.box_footer = QHBoxLayout()

        # add elements to boxes
        # bom button + label
        self.button_bom = QPushButton(Lang.get_string("button_bom"), self)
        self.button_bom.setToolTip(Lang.get_string("button_bom_tooltip"))
        self.button_bom.setFixedSize(Definitions.GUI_WIDTH_BUTTON, Definitions.GUI_HEIGHT_BUTTON)
        self.button_bom.clicked.connect(self.select_file)
        self.label_bom = QLabel(self.file_name_bom, self)
        self.box_header_bom.addWidget(self.button_bom)
        self.box_header_bom.addWidget(self.label_bom)
        self.box_header_bom.addStretch()
        # database button + label
        self.button_database = QPushButton(Lang.get_string("button_database"),self)
        self.button_database.setToolTip(Lang.get_string("button_database_tooltip"))
        self.button_database.setFixedSize(Definitions.GUI_WIDTH_BUTTON, Definitions.GUI_HEIGHT_BUTTON)
        self.button_database.clicked.connect(self.select_database_folder)
        self.label_database = QLabel(self.path_database, self)
        self.box_header_database.addWidget(self.button_database)
        self.box_header_database.addWidget(self.label_database)
        self.box_header_database.addStretch()
        # drop down menu for CAD system
        self.combobox_cad = QComboBox()
        self.combobox_cad.addItems(self.dispatcher.get_cad_system().get_system_names())
        self.combobox_cad.setCurrentIndex(self.combobox_cad.findText(self.dispatcher.get_cad_system().get_name_of_selected_system(),Qt.MatchFixedString))
        self.combobox_cad.setFixedWidth(Definitions.GUI_WIDTH_BUTTON)
        self.combobox_cad.activated[str].connect(self.select_cad_system)
        # button regroup
        self.button_regroup = QPushButton(Lang.get_string("button_regroup"),self)
        self.button_regroup.setToolTip(Lang.get_string("button_regroup_tooltip"))
        self.button_regroup.setEnabled(self.window_settings["view_grouped"])
        self.button_regroup.setFixedSize(Definitions.GUI_WIDTH_BUTTON, Definitions.GUI_HEIGHT_BUTTON)
        self.button_regroup.clicked.connect(self.regroup)
        # checkbox for grouped/ungrouped view
        self.checkbox_grouped = QCheckBox(Lang.get_string("checkbox_grouped"))
        self.checkbox_grouped.setChecked(self.window_settings["view_grouped"])
        self.checkbox_grouped.setEnabled(False)
        self.checkbox_grouped.stateChanged.connect(lambda: self.checkbox_changed(self.checkbox_grouped))
        # export ordering numbers
        self.button_export = QPushButton(Lang.get_string("button_export"),self)
        self.button_export.setToolTip(Lang.get_string("button_export_tooltip"))
        self.button_export.setEnabled(False)
        self.button_export.setFixedSize(Definitions.GUI_WIDTH_BUTTON, Definitions.GUI_HEIGHT_BUTTON)
        self.button_export.clicked.connect(self.export)
        # generate button
        self.button_generate = QPushButton(Lang.get_string("button_generate"),self)
        self.button_generate.setToolTip(Lang.get_string("button_generate_tooltip"))
        self.button_generate.setFixedSize(Definitions.GUI_WIDTH_BUTTON, Definitions.GUI_HEIGHT_BUTTON)
        self.button_generate.clicked.connect(self.generate_matches)
        # label requesting user to select files
        self.label_hint = QLabel(Lang.get_string("label_hint"),self)
        # close button
        self.button_close = QPushButton(Lang.get_string("button_close"), self)
        self.button_close.setToolTip(Lang.get_string("button_close_tooltip"))
        self.button_close.setFixedSize(Definitions.GUI_WIDTH_BUTTON, Definitions.GUI_HEIGHT_BUTTON)
        self.button_close.clicked.connect(QCoreApplication.quit)
        # pack header box
        self.box_header.addLayout(self.box_header_bom)
        self.box_header.addLayout(self.box_header_database)
        # pack command box
        self.box_commands.addWidget(self.combobox_cad)
        self.box_commands.addWidget(self.checkbox_grouped)
        self.box_commands.addStretch()
        self.box_commands.addWidget(self.button_export)
        self.box_commands.addWidget(self.button_regroup)
        self.box_commands.addWidget(self.button_generate)
        # pack body
        self.box_body.addWidget(self.label_hint)
        self.box_body.addStretch()
        self.box_body.setAlignment(Qt.AlignTop)
        self.scroll_widget.setLayout(self.box_body)
        self.scroll_body.setWidget(self.scroll_widget)
        # pack footer
        self.box_footer.addStretch()
        self.box_footer.addWidget(self.button_close)
        # pack window
        self.box_window.addLayout(self.box_header)
        self.box_window.addLayout(self.box_commands)
        self.box_window.addWidget(self.scroll_body)
        self.box_window.addLayout(self.box_footer)

        # set scroll area properties
        self.scroll_body.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll_body.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_body.setWidgetResizable(True)

        # build central widget and select it
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.centralWidget().setLayout(self.box_window)

        # add status bar
        self.status_bar = QStatusBar(self)
        self.setStatusBar(self.status_bar)

        # show window
        self.setGeometry(50,50,1024,768)
        self.setWindowTitle(Lang.get_string("window_title"))
        self.showMaximized()
        self.show()

    def select_file(self):
        self.statusBar().showMessage(Lang.get_string("status_bar_msg_bom_file"))
        file_name_bom, _ = QFileDialog.getOpenFileName(self,Lang.get_string("file_dialog_bom_name"),"",Lang.get_string("file_dialog_bom_type"))
        if file_name_bom:
            self.file_name_bom = file_name_bom
            self.label_bom.setText(file_name_bom)
            self.statusBar().showMessage(Lang.get_string("status_bar_msg_bom_sel_file") + file_name_bom, 5000)
        else:
            self.statusBar().clearMessage()

    def select_database_folder(self):
        self.statusBar().showMessage(Lang.get_string("status_bar_msg_database_folder"))
        path_database = QFileDialog.getExistingDirectory(self,Lang.get_string("file_dialog_database_name"))
        if path_database:
            self.path_database = path_database
            self.label_database.setText(path_database)
            self.statusBar().showMessage(Lang.get_string("status_bar_msg_database_sel_folder") + path_database, 5000)
        else:
            self.statusBar().clearMessage()

    def select_cad_system(self,system):
        self.dispatcher.get_cad_system().select_system(system)

    def generate_matches(self):
        if self.path_database and self.file_name_bom:
            self.statusBar().showMessage(Lang.get_string("status_bar_msg_search_running"))
            self.checkbox_grouped.setEnabled(True)
            self.button_export.setEnabled(True)
            try:
                self.dispatcher.set_bom_file_path(self.file_name_bom)
                self.dispatcher.set_database_path(self.path_database)
                self.dispatcher.find_matches()
                self.statusBar().showMessage(Lang.get_string("status_bar_msg_search_finished"), 5000)
                self.show_matches()
            except Exception as e:
                self.statusBar().showMessage(Lang.get_string("status_bar_msg_error"))
                error_msg = QMessageBox()
                error_msg.setIcon(QMessageBox.Critical)
                error_msg.setText(Lang.get_string("error"))
                error_msg.setInformativeText(e.args[0])
                error_msg.setWindowTitle(Lang.get_string("error"))
                error_msg.exec_()
                raise Exception from e
        else:
            error_msg = QMessageBox()
            error_msg.setIcon(QMessageBox.Critical)
            error_msg.setText(Lang.get_string("error"))
            error_msg.setInformativeText(Lang.get_string("error_msg_file_and_folder"))
            error_msg.setWindowTitle(Lang.get_string("error"))
            error_msg.exec_()
            self.statusBar().clearMessage()

    def show_matches(self):
        # reassign layout reference to "delete" it from widget
        QWidget().setLayout(self.box_body)
        self.box_body = QVBoxLayout()
        self.box_body.setAlignment(Qt.AlignTop)
        self.box_body.addLayout(self.visualization.get_visualization())
        self.box_body.addStretch()
        self.scroll_widget.setLayout(self.box_body)

    def checkbox_changed(self,checkbox):
        if checkbox == self.checkbox_grouped:
            self.window_settings["view_grouped"]=checkbox.isChecked()
            # set button state
            self.button_regroup.setEnabled(checkbox.isChecked())
            # need to regroup, if user selects grouped view
            if checkbox.isChecked():
                self.dispatcher.regroup_parts()
            self.show_matches()

    def regroup(self):
        self.dispatcher.regroup_parts()
        self.show_matches()

    def export(self):
        try:
            # use BOM file to determine folder and filename
            path,filename = os.path.split(self.file_name_bom)
            # remove file ending
            filename,_ = os.path.splitext(filename)
            self.dispatcher.export(path,filename)
            self.statusBar().showMessage(Lang.get_string("status_bar_msg_done"), 2000)
        except Exception as e:
            self.statusBar().showMessage(Lang.get_string("status_bar_msg_error"))
            error_msg = QMessageBox()
            error_msg.setIcon(QMessageBox.Critical)
            error_msg.setText(Lang.get_string("error"))
            error_msg.setInformativeText(e.args[0])
            error_msg.setWindowTitle(Lang.get_string("error"))
            error_msg.exec_()
            raise Exception from e

def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
