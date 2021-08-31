import PyQt5.QtCore as qtc
import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
import pandas as pd
import os
from GenerateReport import MplCanvas, generate_report_objects, AUDITOR_FILE_PATH
from BackEnd import auditor_data_pull, data_pull


def pull_config_files(self):
    self.files = os.listdir(os.getcwd() + "/config_files")
    self.audits = {}
    for x in self.files:
        if ".txt" in x:
            fields = {}
            with open(os.getcwd() + "/config_files/" + x, "r+") as file:
                field_lst = file.readlines()
            for i, y in enumerate(field_lst):
                if i % 2 == 0:
                    fields[y.strip()] = field_lst[i + 1].strip()
            self.audits[fields["Audit_Name"]] = fields
