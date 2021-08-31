import PyQt5.QtWidgets as qtw
from config_processing import create_config_file, pull_config_files, delete_config_file


class DeleteAuditorDialog(qtw.QDialog):
    def __init__(self, sender):
        super().__init__()

        self.setWindowTitle("Delete Auditor")
        qbtn = qtw.QDialogButtonBox.Ok
        self.buttonBox = qtw.QDialogButtonBox(qbtn)
        self.buttonBox.accepted.connect(self.accept)
        sender.delete_auditor_f = qtw.QFrame()
        sender.delete_auditor_l = qtw.QVBoxLayout(sender.delete_auditor_f)
        sender.auditor_combo = qtw.QComboBox()
        sender.delete_auditor_btn = qtw.QPushButton("Delete", clicked=sender.removing_auditor)
        sender.delete_auditor_l.addWidget(sender.auditor_combo)
        sender.delete_auditor_l.addWidget(sender.delete_auditor_btn)
        sender.load_auditors_into_delete_box()

        self.layout = qtw.QVBoxLayout()
        self.layout.addWidget(qtw.QLabel("Select an Auditor to Delete."))
        self.layout.addWidget(sender.delete_auditor_f)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)


class AddAuditorDialog(qtw.QDialog):
    def __init__(self, sender):
        super().__init__()

        self.setWindowTitle("Add Auditor")
        self.sender = sender
        qbtn = qtw.QDialogButtonBox.Ok
        self.buttonBox = qtw.QDialogButtonBox(qbtn)
        self.buttonBox.accepted.connect(self.accept)
        self.create_auditor_management()
        self.layout = qtw.QVBoxLayout()
        self.layout.addWidget(self.sender.add_auditor_f)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    def create_auditor_management(self):
        self.sender.add_auditor_f = qtw.QFrame()
        self.sender.add_auditor_l = qtw.QGridLayout(self.sender.add_auditor_f)
        self.sender.new_auditor_name = qtw.QLineEdit(placeholderText="Auditor Login")
        self.sender.new_auditor_floor = qtw.QComboBox()
        self.sender.new_auditor_floor.addItem("A01")
        self.sender.new_auditor_floor.addItem("A02")
        self.sender.new_auditor_floor.addItem("A03")
        self.sender.new_auditor_floor.addItem("A04")
        self.sender.add_auditor = qtw.QPushButton("Add Auditor",clicked=self.sender.add_new_auditor)
        self.sender.add_auditor.setSizePolicy(qtw.QSizePolicy.Fixed, qtw.QSizePolicy.Fixed)
        self.sender.add_auditor.setFixedWidth(self.sender.horizontal_resolution / 7)
        self.sender.add_auditor_l.addWidget(self.sender.new_auditor_name, 0, 0, 1, 2)
        self.sender.add_auditor_l.addWidget(self.sender.new_auditor_floor, 0, 2, 1, 1)
        self.sender.add_auditor_l.addWidget(qtw.QLabel(), 1, 0, 1, 1)
        self.sender.add_auditor_l.addWidget(self.sender.add_auditor, 1, 1, 1, 1)


class AddAuditConfigDialog(qtw.QDialog):
    def __init__(self, sender):
        super().__init__()
        self.setWindowTitle("Add Audit")
        self.sender = sender
        qbtn = qtw.QDialogButtonBox.Ok
        self.buttonBox = qtw.QDialogButtonBox(qbtn)
        self.create_add_audit_objects()
        self.buttonBox.accepted.connect(self.accept)
        self.layout = qtw.QVBoxLayout()
        self.layout.addWidget(self.sender.add_audit_f)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    def create_add_audit_objects(self):
        self.sender.add_audit_f = qtw.QFrame()
        self.sender.add_audit_l = qtw.QGridLayout(self.sender.add_audit_f)
        self.sender.audit_config_name_lbl = qtw.QLabel("Audit_Name")
        self.sender.audit_config_col_name_lbl = qtw.QLabel("Auditor_Login_Col")
        self.sender.new_audit_name = qtw.QLineEdit(placeholderText="Audit_Name")
        self.sender.new_audit_col_name = qtw.QLineEdit(placeholderText="Auditor_Login_Col")
        self.sender.add_audit_btn = qtw.QPushButton("Add Audit Configuration")
        self.sender.add_audit_btn.clicked.connect(lambda: create_config_file(self.sender))

        self.sender.add_audit_l.addWidget(self.sender.audit_config_name_lbl, 0, 0, 1, 1)
        self.sender.add_audit_l.addWidget(self.sender.new_audit_name, 0, 1, 1, 1)
        self.sender.add_audit_l.addWidget(self.sender.audit_config_col_name_lbl, 1, 0, 1, 1)
        self.sender.add_audit_l.addWidget(self.sender.new_audit_col_name, 1, 1, 1, 1)
        self.sender.add_audit_l.addWidget(self.sender.add_audit_btn, 2, 0, 1, 2)


class DeleteAuditConfigDialog(qtw.QDialog):
    def __init__(self, sender):
        super().__init__()
        self.setWindowTitle("Delete Audit")
        self.sender = sender
        qbtn = qtw.QDialogButtonBox.Ok
        self.buttonBox = qtw.QDialogButtonBox(qbtn)
        self.create_delete_audit_objects()
        self.buttonBox.accepted.connect(self.accept)
        self.layout = qtw.QVBoxLayout()
        self.layout.addWidget(qtw.QLabel("Select an Audit to Delete."))
        self.layout.addWidget(self.sender.delete_audit_f)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    def create_delete_audit_objects(self):
        self.sender.delete_audit_f = qtw.QFrame()
        self.sender.delete_audit_l = qtw.QGridLayout(self.sender.delete_audit_f)
        self.sender.audit_config_combo = qtw.QComboBox()
        self.sender.delete_config_btn = qtw.QPushButton("Delete Audit")
        self.sender.delete_config_btn.clicked.connect(lambda: delete_config_file(self.sender))
        self.sender.populate_delete_audit_combo()

        self.sender.delete_audit_l.addWidget(self.sender.audit_config_combo, 0, 0, 1, 1)
        self.sender.delete_audit_l.addWidget(self.sender.delete_config_btn, 1, 0, 1, 1)

