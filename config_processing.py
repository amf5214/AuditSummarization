import os


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


def create_config_file(self):
    name = self.new_audit_name.text()
    col = self.new_audit_col_name.text()
    with open(os.getcwd() + "/config_files/" + name + ".txt", "w+") as file:
        file.write("Audit_Name\n")
        file.write(name + "\n")
        file.write("Audit_Login_Col\n")
        file.write(col + "\n")
    self.populate_audit_combo()


def delete_config_file(self):
    file = self.audit_config_combo.currentText()
    path = os.getcwd() + "/config_files/" + file + ".txt"
    if os.path.exists(path):
        os.remove(path)
    else:
        print(f"{path} does not exist")
    self.populate_delete_audit_combo()
    self.populate_audit_combo()
