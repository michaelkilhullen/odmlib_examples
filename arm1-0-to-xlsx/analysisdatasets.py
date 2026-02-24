import csv
import os


class AnalysisDatasets:
    HEADERS = ["Result", "Order", "Dataset", "Variables", "Where Clause"]

    def __init__(self, odmlib_mdv, data_path):
        self.mdv = odmlib_mdv
        self.path = data_path
        self.file_name = os.path.join(self.path, "analysisdatasets.csv")

    def extract(self):
        with open(self.file_name, 'w', newline='') as f:
            writer = csv.writer(f, dialect="excel")
            writer.writerow(self.HEADERS)
            #for ig in self.mdv.AnalysisResultDisplays:
            #   writer.writerow([ig.OID, ig.Name, ig.Description.TranslatedText[0]._content, ig.DocumentRef])
