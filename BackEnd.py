import pandas as pd

TEST_PATH = "/Users/austinfraley/Documents/foo_test_data_1.csv"
AUDITOR_PATH = "/Users/austinfraley/PycharmProjects/AuditSummarization/Auditors.csv"
AUDITOR_COL_INDEX_FOO = 0
graph_types = ["Pie Chart", "Line Graph", "Scatter Plot", "Bar Graph"]
graph_by_options = ["Graph By Floor", "Graph By Auditor"]


def data_pull(csv):
    # This is not going to work in the field, because there won't be an index column so will need to be pushed back without index and pulled without one
    return pd.read_csv(csv, index_col=0)


def audit_df_to_dict(file_path, index):
    auditor_df = data_pull(file_path)
    try:
        ind = [i for i, x in enumerate(auditor_df.columns) if x == index][0]
    except IndexError:
        return "ERROR", "ERROR"
    auditor_dict = auditor_df.value_counts().to_dict()
    return auditor_dict, ind


def auditor_data_pull(file_path):
    auditor_data_df = data_pull(file_path)
    auditors = {}
    for x in auditor_data_df.index:
        if auditor_data_df.iloc[x, 0] not in auditors:
            auditors[auditor_data_df.iloc[x, 0]] = auditor_data_df.iloc[x, 1]
    return auditors


def floor_audit_counts(auditor_file_path, audit_file_path, index):
    auditor_dict = auditor_data_pull(auditor_file_path)
    audits_dict, ind = audit_df_to_dict(audit_file_path, index)
    print(audits_dict)
    if audits_dict == "ERROR":
        return "ERROR", "ERROR"
    else:
        new_audits_dict = {x[ind]: audits_dict[x] for x in audits_dict}
        audits_dict = new_audits_dict
        floor_counts = {"A01":0, "A02":0, "A03":0, "A04":0}
        for x in audits_dict:
            if x in auditor_dict:
                floor_counts[auditor_dict[x]] += audits_dict[x]
            else:
                print(f"Auditor ({x}) not found in auditor management file {auditor_file_path}")
        floor_lst = []
        count_lst = []
        for y in floor_counts:
                floor_lst.append(y)
                count_lst.append(floor_counts[y])
        audit_dict = {"floors": floor_lst, "counts": count_lst}
        return floor_counts, audit_dict


if __name__ == "__main__":
    print(auditor_data_pull(AUDITOR_PATH))
    # print(auditor_df_to_dict(TEST_PATH))
    # print(floor_audit_counts(AUDITOR_PATH, TEST_PATH))
