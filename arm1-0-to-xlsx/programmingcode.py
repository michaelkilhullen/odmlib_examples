import csv
import os


class ProgrammingCode:
    HEADERS = ["Result", "Context", "Document", "Code"]

    def __init__(self, odmlib_mdv, data_path):
        self.mdv = odmlib_mdv
        self.path = data_path
        self.file_name = os.path.join(self.path, "programmingcode.csv")

    def extract(self):
        with open(self.file_name, 'w', newline='') as f:
            writer = csv.writer(f, dialect="excel")
            writer.writerow(self.HEADERS)
            #for ig in self.mdv.AnalysisResultDisplays:
            #   writer.writerow([ig.OID, ig.Name, ig.Description.TranslatedText[0]._content, ig.DocumentRef])
