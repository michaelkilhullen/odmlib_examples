from odmlib import define_loader as DL, loader as LD

DEF_FILE = "data/defineV21-SDTM.xml"

loader = LD.ODMLoader(DL.XMLDefineLoader(model_package="define_2_1", ns_uri="http://www.cdisc.org/ns/def/v2.1"))
loader.open_odm_document(DEF_FILE)
root = loader.load_odm()
print(f"Study OID is {root.Study.OID}")
