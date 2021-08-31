import PyQt5.QtCore as qtc
import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
import pandas as pd
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from BackEnd import floor_audit_counts, data_pull, audit_df_to_dict
import os
from BackEnd import graph_types, graph_by_options


AUDITOR_FILE_PATH = os.getcwd() + "/config_files/Auditors.csv"


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, width=5, height=5, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot()
        super(MplCanvas, self).__init__(self.fig)

    def new_plot(self):
        self.axes = self.fig.add_subplot()


class ReportWindow(qtw.QMainWindow):
    back_to_main = qtc.pyqtSignal()

    def __init__(self, foo_filename=None, sled_filename=None):
        super().__init__()
        self.foo_filename = foo_filename
        self.sled_filename = sled_filename
        self.foo_sc = MplCanvas()
        self.sled_sc = MplCanvas()
        self.foo_sc.axes.set_title("FOO Counts")
        self.foo_sc.axes.set_xlabel("Floor")
        self.foo_sc.axes.set_ylabel("Audit Count")
        self.sled_sc.axes.set_title("SLED Counts")
        self.sled_sc.axes.set_xlabel("Floor")
        self.sled_sc.axes.set_ylabel("Audit Count")

        self.root_frame = qtw.QFrame()
        self.primary_layout = qtw.QVBoxLayout(self.root_frame)
        self.setCentralWidget(self.root_frame)
        self.graph_frame = qtw.QFrame()
        self.graph_layout = qtw.QHBoxLayout(self.graph_frame)
        self.total_frame = qtw.QFrame()
        self.total_layout = qtw.QHBoxLayout(self.total_frame)
        self.counts_frame = qtw.QFrame()
        self.counts_layout = qtw.QHBoxLayout(self.counts_frame)
        self.primary_layout.addWidget(self.total_frame)
        self.primary_layout.addWidget(self.graph_frame)
        self.primary_layout.addWidget(self.counts_frame)

        if self.foo_filename is not None:
            try:
                col = self.audits[self.audit_selector_combo.currentText()]["Auditor_Login_Col"]
                index = [i for i, x in enumerate(data_pull(AUDITOR_FILE_PATH).columns) if x == col][0]
                self.graph_layout.addWidget(self.foo_sc)
                self.foo_floor_count, self.foo_floor_count_dict = floor_audit_counts(AUDITOR_FILE_PATH, self.foo_filename, index)
                floor_count_df = pd.DataFrame(self.foo_floor_count_dict)
                self.foo_sc.axes.bar(list(floor_count_df["floors"]), list(floor_count_df["counts"]))
                self.foo_sc.axes.set_yticks(range(0, int(floor_count_df["counts"].max()), 2))
                self.foo_sum = floor_count_df["counts"].sum()
                self.foo_total = qtw.QLabel(f"FOO Audit Total = {self.foo_sum}")
                self.foo_counts = qtw.QLabel(f"A01 = {self.foo_floor_count_dict['counts'][0]} | A02 = {self.foo_floor_count_dict['counts'][1]} | A03 = {self.foo_floor_count_dict['counts'][2]} | A04 = {self.foo_floor_count_dict['counts'][3]}")
                self.foo_total.setFont(qtg.QFont("Helvetica", 30))
                self.foo_total.setAlignment(qtc.Qt.AlignCenter)
                self.foo_counts.setFont(qtg.QFont("Helvetica", 20))
                self.foo_counts.setAlignment(qtc.Qt.AlignCenter)
                self.total_layout.addWidget(self.foo_total)
                self.counts_layout.addWidget(self.foo_counts)

            except FileNotFoundError:
                print("Error: FileName is not valid!")


def generate_report_objects(self, audit_name):
        self.output_sw.setCurrentIndex(1)
        if self.audit_filename is not None:
            try:
                self.foo_sc.axes.set_title(f"{self.audit_selector_combo.currentText()} Counts")
                if self.graph_by_combo.currentText() == graph_by_options[0]:
                    self.foo_floor_count, self.foo_floor_count_dict = floor_audit_counts(AUDITOR_FILE_PATH, self.audit_filename, self.audits[self.audit_selector_combo.currentText()]["Auditor_Login_Col"])
                else:
                    self.foo_floor_count, self.foo_floor_count_dict = audit_df_to_dict(self.audit_filename, self.audits[self.audit_selector_combo.currentText()]["Auditor_Login_Col"])
                if self.foo_floor_count == "ERROR":
                    qtw.QMessageBox.critical(self, "Error", "Error: The Selected Data File Does Not Contain The Auditor Column For The Audit Type That Was Selected!\n\n Please Select Another File Or Select Another Audit Type!")
                    return
                else:
                    if self.graph_by_combo.currentText() == graph_by_options[0]:
                        floor_count_df = pd.DataFrame(self.foo_floor_count_dict)
                        x = list(floor_count_df["floors"])
                        y_s = floor_count_df["counts"]
                        y = list(floor_count_df["counts"])
                    else:
                        auditors = []
                        count = []
                        for i, j in zip(self.foo_floor_count.keys(), self.foo_floor_count.values()):
                            auditors.append(i[0])
                            count.append(j)
                        self.foo_floor_count = {"Auditor": auditors, "Count": count}
                        floor_count_df = pd.DataFrame(self.foo_floor_count)
                        x = list(floor_count_df["Auditor"])
                        y_s = floor_count_df["Count"]
                        y = list(floor_count_df["Count"])

                    if self.choose_graph_type.currentText() in graph_types[1:4]:
                        self.clear_graph_layout()
                        self.foo_sc.axes.clear()
                        self.pie_sc.setParent(self.graph_frame)
                        self.graph_layout.addWidget(self.foo_sc)
                        if self.choose_graph_type.currentText() == graph_types[1]:
                            self.foo_sc.axes.plot(x, y)
                        elif self.choose_graph_type.currentText() == graph_types[2]:
                            self.foo_sc.axes.scatter(x, y)
                        elif self.choose_graph_type.currentText() == graph_types[3]:
                            self.foo_sc.axes.bar(x, y)
                        self.foo_sc.axes.set_yticks(range(0, int(y_s.max())+2, 2))
                        self.foo_sum = y_s.sum()
                        self.foo_total.setText(f"{audit_name} Audit Total = {self.foo_sum}")
                        if self.graph_by_combo.currentText() == graph_by_options[0]:
                            self.foo_counts.setText(f"A01 = {self.foo_floor_count_dict['counts'][0]} | A02 = {self.foo_floor_count_dict['counts'][1]} | A03 = {self.foo_floor_count_dict['counts'][2]} | A04 = {self.foo_floor_count_dict['counts'][3]}")
                            self.foo_sc.axes.set_xlabel("Floor")
                        else:
                            self.foo_sc.axes.set_xlabel("Auditor")
                            self.foo_counts.setText("")
                        self.foo_sc.axes.set_ylabel("Audit Count")
                        if self.graph_by_combo.currentText() == graph_by_options[0]:
                            self.foo_sc.axes.set_xticklabels(x, rotation=0)
                            self.foo_sc.fig.tight_layout()
                        else:
                            self.foo_sc.axes.set_xticklabels(x, rotation=-90)
                            self.foo_sc.fig.tight_layout()
                        self.foo_sc.draw()
                    elif self.choose_graph_type.currentText() == graph_types[0]:
                        self.clear_graph_layout()
                        self.pie_sc.axes.clear()
                        self.pie_sc.setParent(self.graph_frame)
                        self.graph_layout.addWidget(self.pie_sc)
                        self.foo_sum = y_s.sum()
                        lbls = [str(x[i])+": "+str(y[i]) for i in range(0, len(x))]
                        self.pie_sc.axes.pie(y, radius=1.2, labels=x)
                        self.foo_total.setText(f"{audit_name} Audit Total = {self.foo_sum}")
                        self.foo_counts.setText("")
                        self.pie_sc.axes.legend(labels=lbls, loc="upper right")
                        self.pie_sc.fig.tight_layout()
                        self.pie_sc.draw()
            except FileNotFoundError:
                print("Error: FileName is not valid!")



