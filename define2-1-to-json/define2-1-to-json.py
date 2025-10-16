import argparse
import odmlib.define_loader as OL
import odmlib.loader as LD
import odmlib.odm_parser as P
import xmlschema as XSD
import os

JSON_NAME = "odmlib-roundtrip-define.json"

"""
define2-1-to-json.py - an example program using odmlib to convert a Define-XML file into a metadata JSON file
ex. cmd-line args: -d ./data/odmlib-roundtrip-define.xml -p ./data/
ex. cmd-line args: -d ./data/odmlib-roundtrip-define.xml -j define-odmlib-roundtrip.json
ex. cmd-line args: -d ./data/odmlib-roundtrip-define.xml -p ./data/ -v 
    -s "/home/sam/standards/DefineV211/schema/cdisc-define-2.1/define2-1-0.xsd
"""

class Define2Json:
    """ generate a metadata spreadsheet from a Define-XML v2.1 file """
    def __init__(self, define_file, json_path, json_filename=JSON_NAME, language="en"):
        self.define_file = define_file
        self.data_path = json_path
        self.json_filename = json_filename
        self.lang = language
        self.acrf = ""

    def create(self):
        loader = LD.ODMLoader(OL.XMLDefineLoader(model_package="define_2_1", ns_uri="http://www.cdisc.org/ns/def/v2.1"))
        loader.open_odm_document(self.define_file)
        mdv_odmlib = loader.MetaDataVersion()
        study_odmlib = loader.Study()
        self._set_acrf(mdv_odmlib)
        define_odmlib = loader.root()
        define_odmlib.write_json(self.json_filename)


    def _set_acrf(self, mdv):
        if mdv.AnnotatedCRF.DocumentRef:
            self.acrf = mdv.AnnotatedCRF.DocumentRef.leafID
        else:
            for leaf in mdv.leaf:
                if leaf.title and "annotated" in leaf.title._content.lower():
                    self.acrf = leaf.ID
                    break


class DefineValidator:
    """ Define-XML schema validation """
    def __init__(self, schema, define_file):
        """
        :param schema: str - the path and filename for the Define-XML schema
        :param define_file: str - the path and filename for the Define-XML to validate
        """
        self.schema_file = schema
        self.define_file = define_file

    def validate(self):
        """" execute the schema validation and report the results """
        validator = P.ODMSchemaValidator(self.schema_file)
        try:
            validator.validate_file(self.define_file)
            print("define-XML schema validation completed successfully...")
        except XSD.validators.exceptions.XMLSchemaChildrenValidationError as ve:
            print(f"schema validation errors: {ve}")

    def _check_file_existence(self):
        """ throw an error if the schema of Define-XML file cannot be found """
        if not os.path.isfile(self.schema_file):
            raise ValueError("The schema validate flag is set, but the schema file cannot be found.")
        if not os.path.isfile(self.define_file):
            raise ValueError("The define-xml file cannot be found.")


def set_cmd_line_args():
    """
    get the command-line arguments needed to convert the Define-XML input file into JSON
    :return: return the argparse object with the command-line parameters
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--define", help="path and file name of Define-XML v2 input file", required=True,
                        dest="define_file")
    parser.add_argument("-p", "--path", help="path to write the generated JSON file to", required=False,
                        dest="json_path", default="./")
    parser.add_argument("-j", "--json", help="Name of JSON file without path", required=False,
                        dest="json_filename", default=JSON_NAME)
    parser.add_argument("-s", "--schema", help="path and file name of Define-XML schema", dest="schema_file")
    parser.add_argument("-v", "--validate", help="schema validate the Define-XML file", default=False, const=True,
                        nargs='?', dest="is_validate")
    parser.add_argument("-l", "--lang", help="language code", default="en", dest="language", required=False)
    args = parser.parse_args()
    return args


def main():
    """ main driver method that generates an JSON file using tje Define-XML v2.1 metadata """
    args = set_cmd_line_args()
    if args.is_validate:
        validator = DefineValidator(args.schema_file, args.define_file)
        validator.validate()
    d2x = Define2Json(args.define_file, args.json_path, args.json_filename, args.language)
    d2x.create()


if __name__ == "__main__":
    main()
