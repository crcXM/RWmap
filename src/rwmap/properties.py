from typing import Any
import xml.etree.ElementTree as ET


def property_to_xml(name: str, value: Any) -> ET.Element:
    attrs = {"name": name}
    
    if isinstance(value, str):
        if value.startswith("\n"):
            attrs["text"] = value
        else:
            attrs["value"] = value
    elif isinstance(value, bool):
        attrs["type"] = "bool"
        attrs["value"] = "true" if value else "false"
    elif isinstance(value, int):
        attrs["type"] = "int"
        attrs["value"] = str(value)
    elif isinstance(value, float):
        attrs["type"] = "float"
        attrs["value"] = str(value)
    else:
        if value is not None:
            attrs["value"] = str(value)
    
    return ET.Element("property", attrs)


def property_from_xml(elem: ET.Element) -> tuple[str, Any]:
    name = elem.get("name", "")
    raw = elem.get("value") or (elem.text or "").strip() or None
    if raw is None:
        return (name, None)
    
    typ = elem.get("type", "string")
    if typ == "bool":
        val = raw.lower() == "true"
    elif typ == "int":
        val = int(raw)
    elif typ == "float":
        val = float(raw)
    else:
        val = raw
    return (name, val)


def properties_to_xml(properties: dict[str, str]) -> ET.Element:
    elem = ET.Element("properties")
    for name, value in properties.items():
        elem.append(property_to_xml(name, value))
    return elem

def properties_from_xml(elem: ET.Element | None) -> dict[str, str]:
    if elem == None:
        return {}
    return dict(property_from_xml(prop) for prop in elem.findall("property"))
