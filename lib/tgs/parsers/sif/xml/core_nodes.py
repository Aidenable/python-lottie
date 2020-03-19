from xml.dom import minidom
import copy
from uuid import uuid4

from .utils import *


class ObjectRegistry:
    def __init__(self):
        self.registry = {}

    def register_as(self, object, key):
        self.registry[key] = object

    def register(self, object):
        guid = getattr(object, "guid", None)
        if guid is None:
            guid = self.guid()
            object.guid = guid
        self.registry[guid] = object

    @classmethod
    def guid(cls):
        return str(uuid4()).replace("-", "").upper()

    def get_object(self, guid):
        return self.registry[guid]


class XmlDescriptor:
    def __init__(self, name):
        self.name = name
        self.att_name = name.replace("-", "_").replace("[", "_").replace("]", "").replace(".", "_")

    def to_xml(self, obj, parent: minidom.Element, dom: minidom.Document):
        raise NotImplementedError

    def from_xml(self, obj, parent: minidom.Element, registry: ObjectRegistry):
        raise NotImplementedError

    def from_python(self, value):
        raise NotImplementedError

    def initialize_object(self, dict, obj):
        if self.att_name in dict:
            setattr(obj, self.att_name, self.from_python(dict[self.att_name]))
        else:
            setattr(obj, self.att_name, self.default())

    def clean(self, value):
        return self.from_python(value)

    def default(self):
        return None

    def __repr__(self):
        return "%s(%r)" % (self.__class__.__name__, self.name)


class TypedXmlDescriptor(XmlDescriptor):
    def __init__(self, name, type=str, default_value=None, att_name=None):
        super().__init__(name)
        self.type = type
        self.default_value = default_value
        if att_name is not None:
            self.att_name = att_name

    def from_python(self, value):
        if value is None and self.default_value is None:
            return None
        if not value_isinstance(value, self.type):
            return self.type(value)
        return value

    def default(self):
        return copy.deepcopy(self.default_value)


class XmlAttribute(TypedXmlDescriptor):
    def from_xml(self, obj, parent: minidom.Element, registry: ObjectRegistry):
        xml_str = parent.getAttribute(self.name)
        if xml_str:
            setattr(obj, self.att_name, value_from_xml_string(xml_str, self.type))

    def to_xml(self, obj, parent: minidom.Element, dom: minidom.Document):
        value = getattr(obj, self.att_name)
        if value is not None:
            parent.setAttribute(self.name, value_to_xml_string(value, self.type))


class XmlFixedAttribute(XmlDescriptor):
    def __init__(self, name, value, type=str):
        super().__init__(name)
        self.value = value
        self.type = type

    def to_xml(self, obj, parent: minidom.Element, dom: minidom.Document):
        parent.setAttribute(self.name, value_to_xml_string(self.value, self.type))

    def from_python(self, value):
        if value != self.value:
            raise ValueError("Value of %s should be %s, got %s" % (self.name, self.value, value))
        return value

    def from_xml(self, obj, parent: minidom.Element, registry: ObjectRegistry):
        xml_str = parent.getAttribute(self.name)
        setattr(obj, self.att_name, value_from_xml_string(xml_str, self.type))

    def default(self):
        return self.value


class XmlSimpleElement(TypedXmlDescriptor):
    def from_xml(self, obj, parent: minidom.Element, registry: ObjectRegistry):
        cn = xml_first_element_child(parent, self.name, allow_none=True)
        if cn:
            value = value_from_xml_string(xml_text(cn), self.type)
        else:
            value = self.default_value

        setattr(obj, self.att_name, value)

    def to_xml(self, obj, parent: minidom.Element, dom: minidom.Document):
        value = getattr(obj, self.att_name)
        if value is not None:
            parent.appendChild(xml_make_text(dom, self.name, value_to_xml_string(value, self.type)))


class XmlMeta(TypedXmlDescriptor):
    def from_xml(self, obj, parent: minidom.Element, registry: ObjectRegistry):
        for cn in xml_child_elements(parent, "meta"):
            if cn.getAttribute("name") == self.name:
                value = value_from_xml_string(cn.getAttribute("content"), self.type)
                break
        else:
            value = self.default_value

        setattr(obj, self.att_name, value)

    def to_xml(self, obj, parent: minidom.Element, dom: minidom.Document):
        value = getattr(obj, self.att_name)
        if value is not None:
            meta = parent.appendChild(dom.createElement("meta"))
            meta.setAttribute("name", self.name)
            meta.setAttribute("content", value_to_xml_string(value, self.type))
