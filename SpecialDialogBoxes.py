import PyQt5.QtWidgets as qtw


class DeleteAuditorDialog(qtw.QDialog):
    def __init__(self, sender):
        super().__init__()

        self.setWindowTitle("Delete Auditor")
        qbtn = qtw.QDialogButtonBox.Ok
        self.buttonBox = qtw.QDialogButtonBox(qbtn)
        self.buttonBox.accepted.connect(self.accept)
        sender.delete_auditor_f = qtw.QFrame()
        sender.delete_auditor_l = qtw.QHBoxLayout(sender.delete_auditor_f)
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
