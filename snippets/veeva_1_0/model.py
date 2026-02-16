import odmlib.odm_element as OE
import odmlib.typed as T
import odmlib.ns_registry as NS

NS.NamespaceRegistry(prefix="vee", uri="http://www.cdisc.org/ns/veeva/v1.0")

class CodeListItem(OE.ODMElement):
    Code = T.String(required=True)
    Label = T.String(required=True)

class CodeListDef(OE.ODMElement):
    # namespace = "vee"
    Name = T.Name(required=True)
    CodeListItem = T.ODMListObject(element_class=CodeListItem)

class UnitChoice(OE.ODMElement):
    # namespace = "vee"
    Name = T.Name(required=True)
    Label = T.String(required=True)

class UnitDef(OE.ODMElement):
    # namespace = "vee"
    Name = T.Name(required=True)
    UnitChoice = T.ODMListObject(element_class=UnitChoice)


class ItemDef(OE.ODMElement):
    Name = T.Name(required=True)
    Label = T.String(required=True, namespace="vee")
    DataType = T.ValueSetString(required=True)
    Length = T.PositiveInteger()
    Precision = T.NonNegativeInteger(namespace="vee")
    UnknownDay = T.ExtendedValidValues(required=False, valid_values=["Yes", "No"], namespace="vee")
    UnknownMonth = T.ExtendedValidValues(required=False, valid_values=["Yes", "No"], namespace="vee")
    UnknownTime = T.ExtendedValidValues(required=False, valid_values=["Yes", "No"], namespace="vee")
    UnitDef = T.String(required=False, namespace="vee")
    CodeListDef = T.String(required=False, namespace="vee")

class ItemGroupDef(OE.ODMElement):
    Name = T.Name(required=True)
    RepeatMaximum = T.Integer(required=True, namespace="vee")
    # RepeatMaximum = T.Integer(required=True)
    ItemDef = T.ODMListObject(element_class=ItemDef)

    def __len__(self):
        return len(self.ItemDef)

    def __getitem__(self, position):
        return self.ItemDef[position]

    def __iter__(self):
        return iter(self.ItemDef)

class FormDef(OE.ODMElement):
    Name = T.Name(required=True)
    RepeatMaximum = T.Integer(required=True, namespace="vee")
    ItemGroupDef = T.ODMListObject(element_class=ItemGroupDef)

    def __len__(self):
        return len(self.ItemGroupDef)

    def __getitem__(self, position):
        return self.ItemGroupDef[position]

    def __iter__(self):
        return iter(self.ItemGroupDef)

class EventDef(OE.ODMElement):
    # namespace = "vee"
    Name = T.Name(required=True)
    FormDef = T.ODMListObject(element_class=FormDef)

    def __len__(self):
        """ returns the number of FormRefs in an StudyEventDef object as the length """
        return len(self.FormDef)

    def __getitem__(self, position):
        """ creates an iterator from an StudyEventDef object that returns the FormRef in position """
        return self.FormDef[position]

    def __iter__(self):
        return iter(self.FormDef)

class EventGroupDef(OE.ODMElement):
    Name = T.Name(required=True)
    RepeatMaximum = T.Integer(required=True)
    EventDef = T.ODMListObject(element_class=EventDef)

class MetaDataVersion(OE.ODMElement):
    Name = T.Name(required=True)
    Description = T.String(required=False)
    EventGroupDef = T.ODMListObject(element_class=EventGroupDef)
    EventDef = T.ODMListObject(element_class=EventDef)
    FormDef = T.ODMListObject(element_class=FormDef)
    ItemGroupDef = T.ODMListObject(element_class=ItemGroupDef)
    ItemDef = T.ODMListObject(element_class=ItemDef)
    CodeListDef = T.ODMListObject(element_class=CodeListDef)
    UnitDef = T.ODMListObject(element_class=UnitDef)

class Study(OE.ODMElement):
    Name = T.Name(required=True, namespace="vee")
    MetaDataVersion = T.ODMObject(required=True, element_class=MetaDataVersion)


class ODM(OE.ODMElement):
    Description = T.String(required=False)
    FileType = T.ValueSetString(required=True)
    Granularity = T.ValueSetString(required=False)
    Archival = T.ValueSetString(required=False)
    FileOID = T.OID(required=True)
    CreationDateTime = T.DateTimeString(required=True)
    PriorFileOID = T.OIDRef(required=False)
    AsOfDateTime = T.DateTimeString(required=False)
    ODMVersion = T.ValueSetString(required=False)
    Originator = T.String(required=False)
    SourceSystem = T.String(required=False)
    SourceSystemVersion = T.String(required=False)
    schemaLocation = T.String(required=False, namespace="xs")
    Study = T.ODMListObject(element_class=Study)
