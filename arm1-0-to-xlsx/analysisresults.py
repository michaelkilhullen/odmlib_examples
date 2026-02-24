import csv
import os


class AnalysisResults:
    HEADERS = ["OID", "ParameterOID", "Description", "Reason", "Purpose", "DisplayOID", "Documentation", "Document",
               "Pages", "Title", "DatasetComment"]

    def __init__(self, odmlib_display, data_path):
        self.mdv = odmlib_display
        self.path = data_path
        self.file_name = os.path.join(self.path, "analysisresults.csv")

    def extract(self):
        with open(self.file_name, 'w', newline='') as f:
            writer = csv.writer(f, dialect="excel")
            writer.writerow(self.HEADERS)
            for display in self.mdv.ResultDisplay:
                for ig in display.AnalysisResult:
                    writer.writerow([ig.OID, ig.ParameterOID, ig.Description.TranslatedText[0]._content,
                        ig.AnalysisReason, ig.AnalysisPurpose, display.OID,
                        ig.Documentation.Description.TranslatedText[0]._content, ig.Documentation.DocumentRef[0].leafID,
                        ig.Documentation.DocumentRef[0].PDFPageRef[0].PageRefs,
                        ig.Documentation.DocumentRef[0].PDFPageRef[0].Title, ig.AnalysisDatasets.CommentOID])
