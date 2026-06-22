from typing import Any, Dict
import xml.etree.ElementTree as ET


class Text(str):
    pass


def property_to_xml(name: str, value: Any) -> ET.Element:
    attrs = {"name": name}

    match value:
        case Text():
            elem = ET.Element("property", attrs)
            elem.text = value
            return elem
        case None:
            return ET.Element("property", attrs)
        case bool():
            attrs["type"] = "bool"
            attrs["value"] = "true" if value else "false"
        case int():
            attrs["type"] = "int"
            attrs["value"] = str(value)
        case float():
            attrs["type"] = "float"
            attrs["value"] = str(value)
        case _:
            attrs["value"] = str(value)

    return ET.Element("property", attrs)


def property_from_xml(elem: ET.Element) -> tuple[str, Any]:
    name = elem.attrib["name"]
    raw = elem.get("value")

    if raw is None:
        text = elem.text
        return (name, Text(text)) if text is not None else (name, None)

    match elem.get("type"):
        case "bool":
            val = raw.lower() == "true"
        case "int":
            val = int(raw)
        case "float":
            val = float(raw)
        case _:
            val = raw

    return (name, val)


def properties_to_xml(properties: Dict[str, Any]) -> ET.Element:
    root = ET.Element("properties")
    for name, value in properties.items():
        root.append(property_to_xml(name, value))
    return root


def properties_from_xml(elem: ET.Element | None) -> Dict[str, Any]:
    if elem is None:
        return {}
    return dict(property_from_xml(prop) for prop in elem.findall("property"))
