import PyQt5.QtCore as qtc
import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
import pandas as pd
from GenerateReport import MplCanvas, generate_report_objects, AUDITOR_FILE_PATH
from BackEnd import auditor_data_pull, data_pull
import os
from config_processing import pull_config_files
from BackEnd import graph_types
from SpecialDialogBoxes import DeleteAuditorDialog, AddAuditorDialog, AddAuditConfigDialog, DeleteAuditConfigDialog


SPHERES_PATH = os.getcwd() + "/media/amazon_spheres.jpg"
LOGO_PATH = os.getcwd() + "/media/amazon_logo.png"


class PrimaryWindow(qtw.QMainWindow):

    def __init__(self, hor=None, ver=None):
        super().__init__()
        self.setWindowTitle("Audit Summarizer")
        self.setWindowIcon(qtg.QIcon(LOGO_PATH))
        self.audit_filename = None

        self.horizontal_resolution = hor
        self.vertical_resolution = ver

        self.setFixedHeight(self.vertical_resolution/1.6)
        self.setFixedWidth(self.horizontal_resolution/2)

        self.menu = qtw.QMenuBar(self)
        self.setMenuBar(self.menu)
        self.menu.setStyleSheet("background-color: transparent")
        # self.menu.setNativeMenuBar(True)
        self.managing_auditor_menu = qtw.QMenu("Manage Auditors")
        self.managing_audits_menu = qtw.QMenu("Manage Audits")

        self.view_auditors = qtw.QAction("View Auditors")
        self.select_auditor_file = qtw.QAction("Select Auditor File")
        self.add_auditor_action = qtw.QAction("Add Auditor")
        self.delete_auditor_action = qtw.QAction("Delete Auditor")
        self.manage_audits = qtw.QAction("Manage Audits")
        self.add_audit = qtw.QAction("Add Audit Configuration")
        self.delete_audit = qtw.QAction("Delete Audit Configuration")
        self.view_auditors.triggered.connect(self.open_auditor_menu)
        self.add_auditor_action.triggered.connect(lambda: AddAuditorDialog(self).exec())
        self.delete_auditor_action.triggered.connect(lambda: DeleteAuditorDialog(self).exec())
        self.select_auditor_file.triggered.connect(lambda: self.get_file_data("Auditor"))
        self.manage_audits.triggered.connect(self.fill_audit_manager_widget)
        self.add_audit.triggered.connect(lambda: AddAuditConfigDialog(self).exec())
        self.delete_audit.triggered.connect(lambda: DeleteAuditConfigDialog(self).exec())

        self.managing_auditor_menu.addAction(self.view_auditors)
        self.managing_auditor_menu.addAction(self.select_auditor_file)
        self.managing_auditor_menu.addAction(self.add_auditor_action)
        self.managing_auditor_menu.addAction(self.delete_auditor_action)
        self.managing_audits_menu.addAction(self.manage_audits)
        self.managing_audits_menu.addAction(self.add_audit)
        self.managing_audits_menu.addAction(self.delete_audit)

        self.menu.addMenu(self.managing_auditor_menu)
        self.menu.addMenu(self.managing_audits_menu)

        self.root = qtw.QFrame()
        self.setCentralWidget(self.root)
        self.primary_l = qtw.QHBoxLayout(self.root)

        self.audit_f = qtw.QFrame()
        self.audit_l = qtw.QVBoxLayout(self.audit_f)
        self.back_btn = qtw.QPushButton("Back")
        self.back_btn.setSizePolicy(qtw.QSizePolicy.Fixed, qtw.QSizePolicy.Fixed)
        self.back_btn.setFixedWidth(self.horizontal_resolution / 8)
        self.back_btn.clicked.connect(self.go_back)

        self.output_sw = qtw.QStackedWidget()
        self.auditor_view = qtw.QScrollArea()
        self.report_view = qtw.QScrollArea()

        self.spheres_jpg = qtg.QPixmap(SPHERES_PATH)
        self.spheres_lbl = qtw.QLabel()
        self.spheres_lbl.setPixmap(self.spheres_jpg)

        self.home_f = qtw.QFrame()
        self.home_l = qtw.QVBoxLayout(self.home_f)
        self.home_l.addWidget(self.spheres_lbl)
        self.auditor_home_f = qtw.QFrame()
        self.auditor_home_l = qtw.QVBoxLayout(self.auditor_home_f)
        self.auditor_view_l = qtw.QFormLayout(self.auditor_view)
        self.report_view_l = qtw.QVBoxLayout(self.report_view)
        self.auditor_view.setVerticalScrollBarPolicy(qtc.Qt.ScrollBarAlwaysOn)
        self.auditor_view.setHorizontalScrollBarPolicy(qtc.Qt.ScrollBarAlwaysOn)
        self.auditor_view.setWidgetResizable(True)
        self.auditor_view.setFrameShape(qtw.QFrame.NoFrame)

        self.report_view.setVerticalScrollBarPolicy(qtc.Qt.ScrollBarAlwaysOn)
        self.report_view.setHorizontalScrollBarPolicy(qtc.Qt.ScrollBarAlwaysOn)
        self.report_view.setWidgetResizable(True)
        self.report_view.setFrameShape(qtw.QFrame.NoFrame)

        self.audit_management_f = qtw.QFrame()
        self.audit_management_l = qtw.QVBoxLayout(self.audit_management_f)
        self.audit_manager = qtw.QTabWidget()
        self.audit_management_l.addWidget(self.audit_manager)
        self.auditor_home_l.addWidget(self.auditor_view)

        self.output_sw.addWidget(self.auditor_home_f)
        self.output_sw.addWidget(self.report_view)
        self.output_sw.addWidget(self.home_f)
        self.output_sw.addWidget(self.audit_management_f)
        self.output_sw.setCurrentIndex(2)

        self.primary_l.addWidget(self.audit_f)
        self.primary_l.addWidget(self.output_sw)

        self.audit_data_vmenu()

        self.create_report_objects()

        self.audit_l.addStretch()
        self.audit_l.addWidget(self.back_btn)

        self.show()

    def add_new_auditor(self):
        if self.new_auditor_name.text() != "" and self.new_auditor_name.text() != " ":
            auditors = data_pull(AUDITOR_FILE_PATH)
            new_row = {"Auditor":self.new_auditor_name.text(), "Floor":self.new_auditor_floor.currentText()}
            auditors = auditors.append(new_row, ignore_index=True)
            auditors.reset_index(drop=True, inplace=True)
            auditors.to_csv(AUDITOR_FILE_PATH)
            self.open_auditor_menu()

    def removing_auditor(self):
        auditors = data_pull(AUDITOR_FILE_PATH)
        auditor = self.auditor_combo.currentText()
        ind = [i for i, x in enumerate(auditors.iloc[:, 0]) if x == auditor]
        auditors.drop(ind, inplace=True)
        auditors.reset_index(drop=True, inplace=True)
        auditors.to_csv(AUDITOR_FILE_PATH)
        self.open_auditor_menu()

    def load_auditors_into_delete_box(self):
        self.auditor_combo.clear()
        auditors = data_pull(AUDITOR_FILE_PATH)
        auditors_dict = auditors.to_dict()
        auditors_user = auditors_dict["Auditor"]
        for x in auditors_user:
            self.auditor_combo.addItem(auditors_user[x])

    def audit_data_vmenu(self):
        self.audit_widgets = []
        self.audit_selector_combo = qtw.QComboBox()
        self.audit_widgets.append(self.audit_selector_combo)
        self.populate_audit_combo()
        self.add_data = qtw.QPushButton("Add Data")
        self.add_data.clicked.connect(lambda: self.get_file_data(self.audit_selector_combo.currentText()))
        self.audit_widgets.append(self.add_data)
        self.generate_report_pb = qtw.QPushButton("Generate Report")
        self.generate_report_pb.clicked.connect(lambda: generate_report_objects(self, self.audit_selector_combo.currentText()))
        self.audit_widgets.append(self.generate_report_pb)
        self.choose_graph_type = qtw.QComboBox()
        for x in graph_types[:]:
            self.choose_graph_type.addItem(x)
        self.choose_graph_type.setCurrentIndex(2)
        self.audit_widgets.append(self.choose_graph_type)
        self.audit_l.addWidget(self.audit_selector_combo)
        self.audit_l.addWidget(self.add_data)
        self.audit_l.addWidget(self.choose_graph_type)
        self.audit_l.addWidget(self.generate_report_pb)
        self.audit_l.addStretch()

        for x in self.audit_widgets:
            x.setSizePolicy(qtw.QSizePolicy.Fixed, qtw.QSizePolicy.Fixed)
            x.setFixedWidth(self.horizontal_resolution/8)

    def get_file_data(self, type):
        audit_filename, acceptance = qtw.QFileDialog.getOpenFileName(self, f"Select {type} data csv file")
        if ".csv" in audit_filename:
            if type == "Auditor":
                global AUDITOR_FILE_PATH
                AUDITOR_FILE_PATH = audit_filename
            else:
                self.audit_filename = audit_filename
        else:
            qtw.QMessageBox.critical(self, "File Error", "Error: The file that you selected is not a valid file type!\nPlease select a csv file")

    def populate_audit_combo(self):
        pull_config_files(self)
        self.audit_selector_combo.clear()
        for x in self.audits:
            self.audit_selector_combo.addItem(x)

    def create_report_objects(self):
        self.foo_sc = MplCanvas()
        self.pie_sc = MplCanvas()
        self.foo_sc.axes.axis("off")
        self.graph_frame = qtw.QFrame()
        self.graph_layout = qtw.QHBoxLayout(self.graph_frame)
        self.total_frame = qtw.QFrame()
        self.total_layout = qtw.QHBoxLayout(self.total_frame)
        self.counts_frame = qtw.QFrame()
        self.counts_layout = qtw.QHBoxLayout(self.counts_frame)
        self.save_fig_frame = qtw.QFrame()
        self.save_fig_layout = qtw.QGridLayout(self.save_fig_frame)
        self.save_fig_btn = qtw.QPushButton("Save Graph")
        self.save_fig_layout.addWidget(qtw.QLabel(), 0, 0)
        self.save_fig_layout.addWidget(self.save_fig_btn, 0, 1)
        self.save_fig_layout.addWidget(qtw.QLabel(), 0, 2)
        self.save_fig_btn.clicked.connect(self.save_fig_func)
        self.report_view_l.addWidget(self.total_frame)
        self.report_view_l.addWidget(self.graph_frame)
        self.report_view_l.addWidget(self.counts_frame)
        self.report_view_l.addWidget(self.save_fig_frame)
        self.foo_total = qtw.QLabel()
        self.foo_counts = qtw.QLabel()
        self.total_layout.addWidget(self.foo_total)
        self.counts_layout.addWidget(self.foo_counts)
        self.foo_total.setFont(qtg.QFont("Helvetica", 30))
        self.foo_total.setAlignment(qtc.Qt.AlignCenter)
        self.foo_counts.setFont(qtg.QFont("Helvetica", 20))
        self.foo_counts.setAlignment(qtc.Qt.AlignCenter)

    def open_auditor_menu(self):
        self.output_sw.setCurrentIndex(0)
        self.delete_all_widgets(self.auditor_view_l)
        try:
            self.auditors = data_pull(AUDITOR_FILE_PATH)
            self.auditor_management_widgets = {}
            for i in self.auditors.index:
                self.login = qtw.QLineEdit(self.auditors.iloc[i, 0])
                self.login.editingFinished.connect(lambda: self.data_change())
                self.auditor_management_widgets[self.login] = i
                floor = qtw.QComboBox()
                self.auditor_management_widgets[floor] = i
                floor.currentTextChanged.connect(lambda: self.floor_change())
                floor.addItem("A01")
                floor.addItem("A02")
                floor.addItem("A03")
                floor.addItem("A04")
                floor.setCurrentText(self.auditors.iloc[i, 1])
                floor.setFont(qtg.QFont("Helvetica", 20))
                self.login.setFont(qtg.QFont("Helvetica", 20))
                self.auditor_view_l.addRow(self.login, floor)
        except IndexError:
            qtw.QMessageBox.critical(self, "File Error", "Error: The Auditor File You Selected Is Not a Valid Auditor File\nPlease Try Again!")
            self.output_sw.setCurrentIndex(2)

    def go_back(self):
        self.output_sw.setCurrentIndex(2)

    def delete_all_widgets(self, layout):
        for i in reversed(range(layout.count())):
            layout.itemAt(i).widget().deleteLater()

    def data_change(self):
        auditors = data_pull(AUDITOR_FILE_PATH)
        ind = int(self.auditor_management_widgets[self.sender()])
        auditors.iloc[ind, 0] = self.sender().text()
        auditors.to_csv(AUDITOR_FILE_PATH)

    def floor_change(self):
        try:
            auditors = data_pull(AUDITOR_FILE_PATH)
            ind = int(self.auditor_management_widgets[self.sender()])
            auditors.iloc[ind, 1] = self.sender().currentText()
            auditors.to_csv(AUDITOR_FILE_PATH)
        except IndexError:
            qtw.QMessageBox.critical(self, "File Error", "Error: The Auditor File You Selected Is Not a Valid Auditor File\nPlease Try Again!")
            self.output_sw.setCurrentIndex(2)

    def save_fig_func(self):
        pic_filename, acceptance = qtw.QFileDialog.getSaveFileName(self, "Select where you would like to save the image.")
        if self.graph_layout.itemAt(0).widget() == self.foo_sc:
            self.foo_sc.fig.savefig(pic_filename)
        elif self.graph_layout.itemAt(0).widget() == self.pie_sc:
            self.pie_sc.fig.savefig(pic_filename)

    def fill_audit_manager_widget(self):
        self.output_sw.setCurrentIndex(3)
        self.delete_tabs()
        pull_config_files(self)
        for x in self.audits:
            audit_tab = qtw.QFrame()
            audit_tab_l = qtw.QFormLayout(audit_tab)
            for i, y in enumerate(self.audits[x]):
                if i == 0:
                    audit_tab_l.addRow(qtw.QLabel(y + ": "), qtw.QLabel(self.audits[x][y]))
                else:
                    audit_tab_l.addRow(qtw.QLabel(y + ": "), qtw.QLineEdit(self.audits[x][y], readOnly=False, editingFinished=lambda: self.update_config_file(y)))
            self.audit_manager.addTab(audit_tab, x)

    def update_config_file(self, y):
        pull_config_files(self)
        widget = self.audit_manager.currentWidget().layout().takeRow(0).fieldItem.widget().text()
        file_path = os.getcwd() + "/config_files/" + str(widget) + ".txt"
        with open(file_path, "w") as file_1:
            file_1.truncate()
        with open(file_path, "a") as file:
            details = self.audits[widget]
            details[y] = self.sender().text()
            for x in details:
                file.write(x + "\n")
                file.write(details[x] + "\n")
        self.fill_audit_manager_widget()

    def delete_tabs(self):
        for x in range(0, self.audit_manager.count()):
            self.audit_manager.widget(x).deleteLater()

    def clear_graph_layout(self):
        for x in range(0, self.graph_layout.count()):
            widget = self.graph_layout.itemAt(x).widget()
            self.graph_layout.removeWidget(widget)
            widget.setParent(None)

    def populate_delete_audit_combo(self):
        self.audit_config_combo.clear()
        pull_config_files(self)
        for x in self.audits.keys():
            self.audit_config_combo.addItem(x)
