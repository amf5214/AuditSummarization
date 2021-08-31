import PyQt5.QtCore as qtc
import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
import pandas as pd
from GenerateReport import MplCanvas, ReportWindow


class ControllerWindow(qtw.QMainWindow):
    def __init__(self):
        super().__init__()

        self.foo_filename = None
        self.sled_filename = None

        self.root = qtw.QTabWidget(movable=True)
        self.setCentralWidget(self.root)
        self.create_audit_interface()

        self.show()

    def create_audit_interface(self):
        self.managing_auditors_tab = qtw.QFrame()
        self.managing_auditors_layout = qtw.QGridLayout(self.managing_auditors_tab)

        self.audits_tab = qtw.QFrame()
        self.audits_layout = qtw.QGridLayout(self.audits_tab)

        self.root.addTab(self.audits_tab, "HOME")
        self.root.addTab(self.managing_auditors_tab, "AUDITORS")
        self.root.setCurrentWidget(self.audits_tab)
        self.create_auditor_management_tab()

        self.add_foo_data = qtw.QPushButton("ADD FOO DATA", clicked=self.get_foo_file_data)
        self.add_sled_data = qtw.QPushButton("ADD SLED DATA", clicked=self.get_sled_file_data)
        self.generate_report = qtw.QPushButton("GENERATE REPORT", clicked=self.generate_report_fun)

        self.audits_layout.addWidget(self.add_foo_data, 0, 0, 1, 1)
        self.audits_layout.addWidget(self.add_sled_data, 0, 1, 1, 1)
        self.audits_layout.addWidget(self.generate_report, 1, 0, 1, 2)

    def generate_report_fun(self):
        self.root.setTabVisible(2, True)
        self.report_window = ReportWindow(self.foo_filename, self.sled_filename)
        self.report_window.back_to_main.connect(self.come_back_from_report)
        self.hide()
        self.report_window.show()

    def come_back_from_report(self):
        self.report_window.close()
        self.show()

    def get_foo_file_data(self):
        foo_filename, acceptance = qtw.QFileDialog.getOpenFileName(self, "Select FOO data csv file")
        if ".csv" in foo_filename or ".xlsx" in foo_filename:
            self.foo_filename = foo_filename

    def get_sled_file_data(self):
        sled_filename, acceptance = qtw.QFileDialog.getOpenFileName(self, "Select SLED data csv file")
        if ".csv" in sled_filename or ".xlsx" in sled_filename:
            self.sled_filename = sled_filename

    def create_auditor_management_tab(self):
        self.add_auditor = qtw.QPushButton("Add Auditor")
        self.modify_auditor = qtw.QPushButton("Modify Auditor")
        self.delete_auditor = qtw.QPushButton("Delete Auditor")
        self.view_auditor = qtw.QPushButton("View Auditors")
        self.managing_auditors_layout.addWidget(self.add_auditor, 1, 0, 1, 1)
        self.managing_auditors_layout.addWidget(self.modify_auditor, 0, 1, 1, 1)
        self.managing_auditors_layout.addWidget(self.delete_auditor, 1, 1, 1, 1)
        self.managing_auditors_layout.addWidget(self.view_auditor, 0, 0, 1, 1)

