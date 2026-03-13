import xml.etree.ElementTree as ET

from typing import Optional, Any

class Property:

    def __init__(
        self,
        name: str,
        value: Any = None,
        type: Optional[str] = None,
        text: Optional[str] = None
    ):
        self.name = name
        self.value = value
        self.text = text
        if type is not None:
            self.type = type
        elif value is not None:
            if isinstance(value, bool):
                self.type = "bool"
            elif isinstance(value, int):
                self.type = "int"
            elif isinstance(value, float):
                self.type = "float"
            else:
                self.type = "string"
        else:
            self.type = "string"

    def to_xml(self, parent: ET.Element) -> None:
        attrs = {"name": self.name}
        if self.type != "string":
            attrs["type"] = self.type
        if self.value is not None:
            if self.type == "bool":
                val = "true" if self.value else "false"
            elif self.type in ("int", "float"):
                val = str(self.value)
            else:
                val = str(self.value)
            attrs["value"] = val
            ET.SubElement(parent, "property", attrs)
        elif self.text is not None:
            elem = ET.SubElement(parent, "property", attrs)
            elem.text = self.text
        else:
            ET.SubElement(parent, "property", attrs)

    @classmethod
    def from_xml(cls, elem: ET.Element) -> 'Property':
        name = elem.get("name", "")
        value = elem.get("value")
        typ = elem.get("type", "string")
        text = elem.text.strip() if elem.text else None
        if value is not None:
            if typ == "bool":
                val = value.lower() == "true"
            elif typ == "int":
                val = int(value)
            elif typ == "float":
                val = float(value)
            else:
                val = value
            return cls(name, val, typ)
        elif text is not None:
            return cls(name, text=text, type=typ)
        else:
            return cls(name)

