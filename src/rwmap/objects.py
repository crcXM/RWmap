import xml.etree.ElementTree as ET
from typing import List, Dict, Optional, Any, Tuple

from .properties import Property

class Shape:

    def __init__(self, type: str, points: Optional[List[Tuple[int, int]]] = None):
        self.type = type
        self.points = points

    def to_xml(self, parent: ET.Element) -> None:
        if self.type == "point":
            ET.SubElement(parent, "point")
        elif self.type == "ellipse":
            ET.SubElement(parent, "ellipse")
        elif self.type in ("polygon", "polyline") and self.points:
            points_str = " ".join(f"{x},{y}" for x, y in self.points)
            ET.SubElement(parent, self.type, {"points": points_str})


class Object:

    def __init__(
        self,
        name: str = "",
        type: str = "",
        x: float = 0,
        y: float = 0,
        width: float = 1,
        height: float = 1,
        rotation: float = 0,
        visible: bool = True,
        shape: Optional[Shape] = None,
        gid: Optional[int] = None,
        text: Optional[str] = None,
        properties: Optional[List[Property]] = None,
        id: Optional[int] = None,
    ):
        self.id = id
        self.name = name
        self.type = type
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rotation = rotation
        self.visible = visible
        self.shape = shape
        self.gid = gid
        self.text = text
        self.properties = properties or []

    def set(self, **kwargs: Any) -> 'Object':
        for k, v in kwargs.items():
            self.properties = [p for p in self.properties if p.name != k]
            self.properties.append(Property(k, v))
        return self

    def add_property(self, name: str, value: Any, type: Optional[str] = None) -> 'Object':
        self.properties = [p for p in self.properties if p.name != name]
        self.properties.append(Property(name, value, type))
        return self

    def copy_xy_from(self, other: 'Object') -> 'Object':
        self.x = other.x
        self.y = other.y
        return self

    def copy_wh_from(self, other: 'Object') -> 'Object':
        self.width = other.width
        self.height = other.height
        return self

    def copy_xywh_from(self, other: 'Object') -> 'Object':
        self.x = other.x
        self.y = other.y
        self.width = other.width
        self.height = other.height
        return self

    @classmethod
    def from_xml(cls, elem: ET.Element) -> 'Object':
        obj = cls(
            id=int(elem.get("id", 0)) if elem.get("id") else None,
            name=elem.get("name", ""),
            type=elem.get("type", ""),
            x=float(elem.get("x", 0)),
            y=float(elem.get("y", 0)),
            width=float(elem.get("width", 1)),
            height=float(elem.get("height", 1)),
            rotation=float(elem.get("rotation", 0)),
            visible=elem.get("visible", "1") != "0",
            gid=int(elem.get("gid")) if elem.get("gid") else None, #type: ignore
        )
        shape_elem = None
        for shape_tag in ["point", "ellipse", "polygon", "polyline"]:
            found = elem.find(shape_tag)
            if found is not None:
                shape_elem = found
                break
        if shape_elem is not None:
            tag = shape_elem.tag
            if tag == "point":
                obj.shape = Shape("point")
            elif tag == "ellipse":
                obj.shape = Shape("ellipse")
            elif tag in ("polygon", "polyline"):
                points_str = shape_elem.get("points", "")
                points: List[Tuple[int, int]] = []
                if points_str:
                    for pair in points_str.split():
                        if ',' in pair:
                            x_str, y_str = pair.split(',')
                            points.append((int(float(x_str)), int(float(y_str))))
                obj.shape = Shape(tag, points if points else None)
        text_elem = elem.find("text")
        if text_elem is not None:
            obj.text = text_elem.text or ""
        props_elem = elem.find("properties")
        if props_elem is not None:
            for prop_elem in props_elem.findall("property"):
                obj.properties.append(Property.from_xml(prop_elem))
        return obj

    def to_xml(self) -> ET.Element:
        attrs: Dict[str, str] = {}
        if self.id is not None:
            attrs["id"] = str(self.id)
        if self.name:
            attrs["name"] = self.name
        if self.type:
            attrs["type"] = self.type
        if self.gid is not None:
            attrs["gid"] = str(self.gid)
        attrs["x"] = str(self.x)
        attrs["y"] = str(self.y)
        if self.width != 1:
            attrs["width"] = str(self.width)
        if self.height != 1:
            attrs["height"] = str(self.height)
        if self.rotation != 0:
            attrs["rotation"] = str(self.rotation)
        if not self.visible:
            attrs["visible"] = "0"
        elem = ET.Element("object", attrs)
        if self.shape:
            self.shape.to_xml(elem)
        if self.text is not None:
            text_elem = ET.SubElement(elem, "text")
            text_elem.text = self.text
        if self.properties:
            props_elem = ET.SubElement(elem, "properties")
            for prop in self.properties:
                prop.to_xml(props_elem)
        return elem


class ObjectGroup:

    def __init__(
        self,
        name: str = "",
        objects: Optional[List[Object]] = None,
        color: Optional[str] = None,
        opacity: float = 1.0,
        visible: bool = True,
        offsetx: float = 0.0,
        offsety: float = 0.0,
        properties: Optional[List[Property]] = None,
    ):
        self.name = name
        self.objects = objects or []
        self.color = color
        self.opacity = opacity
        self.visible = visible
        self.offsetx = offsetx
        self.offsety = offsety
        self.properties = properties or []

    def add(self, obj: Object) -> 'ObjectGroup':
        self.objects.append(obj)
        return self

    def extend(self, objs: List[Object]) -> 'ObjectGroup':
        self.objects.extend(objs)
        return self

    def remove(self, obj: Object) -> 'ObjectGroup':
        if obj in self.objects:
            self.objects.remove(obj)
        return self

    def clear(self) -> 'ObjectGroup':
        self.objects.clear()
        return self

    def find(self, name: str = None, type: str = None, id: int = None) -> Optional[Object]: #type: ignore
        for obj in self.objects:
            if name is not None and obj.name != name:
                continue
            if type is not None and obj.type != type:
                continue
            if id is not None and obj.id != id:
                continue
            return obj
        return None

    def find_all(self, name: str = None, type: str = None) -> List[Object]: #type: ignore
        return [obj for obj in self.objects
                if (name is None or obj.name == name) and
                   (type is None or obj.type == type)]

    def set(self, **kwargs: Any) -> 'ObjectGroup':
        for k, v in kwargs.items():
            self.properties = [p for p in self.properties if p.name != k]
            self.properties.append(Property(k, v))
        return self

    @classmethod
    def from_xml(cls, elem: ET.Element) -> 'ObjectGroup':
        og = cls(
            name=elem.get("name", ""),
            color=elem.get("color"),
            opacity=float(elem.get("opacity", 1.0)),
            visible=elem.get("visible", "1") != "0",
            offsetx=float(elem.get("offsetx", 0)),
            offsety=float(elem.get("offsety", 0)),
        )
        for obj_elem in elem.findall("object"):
            og.objects.append(Object.from_xml(obj_elem))
        props_elem = elem.find("properties")
        if props_elem is not None:
            for prop_elem in props_elem.findall("property"):
                og.properties.append(Property.from_xml(prop_elem))
        return og

    def to_xml(self) -> ET.Element:
        attrs = {"name": self.name}
        if self.color:
            attrs["color"] = self.color
        if self.opacity != 1.0:
            attrs["opacity"] = str(self.opacity)
        if not self.visible:
            attrs["visible"] = "0"
        if self.offsetx != 0:
            attrs["offsetx"] = str(self.offsetx)
        if self.offsety != 0:
            attrs["offsety"] = str(self.offsety)
        elem = ET.Element("objectgroup", attrs)
        if self.properties:
            props_elem = ET.SubElement(elem, "properties")
            for prop in self.properties:
                prop.to_xml(props_elem)
        for obj in self.objects:
            elem.append(obj.to_xml())
        return elem



