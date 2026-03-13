import xml.etree.ElementTree as ET
from typing import List, Dict, Optional
import os

from .properties import Property
from .tiles import Tileset, Tile
from .objects import ObjectGroup
from .layers import Layer


class Map:

    def __init__(self, path: Optional[str] = None):
        self.path = path
        self.version: str = "1.2"
        self.orientation: str = "orthogonal"
        self.renderorder: str = "right-down"
        self.width: int = 0
        self.height: int = 0
        self.tilewidth: int = 1
        self.tileheight: int = 1
        self.nextobjectid: int = 1
        self.properties: List[Property] = []
        self.tilesets: List[Tileset] = []
        self.layers: Dict[str, Layer] = {}
        self.objectgroups: Dict[str, ObjectGroup] = {}
        if path and os.path.exists(path):
            self.load(path)

    def load(self, path: str) -> 'Map':
        self.path = path
        tree = ET.parse(path)
        root = tree.getroot()
        self.version = root.get("version", "1.2")
        self.orientation = root.get("orientation", "orthogonal")
        self.renderorder = root.get("renderorder", "right-down")
        self.width = int(root.get("width", 0))
        self.height = int(root.get("height", 0))
        self.tilewidth = int(root.get("tilewidth", 1))
        self.tileheight = int(root.get("tileheight", 1))
        self.nextobjectid = int(root.get("nextobjectid", 1))
        props_elem = root.find("properties")
        if props_elem is not None:
            for prop_elem in props_elem.findall("property"):
                self.properties.append(Property.from_xml(prop_elem))
        self.tilesets = [Tileset.from_xml(ts_elem) for ts_elem in root.findall("tileset")]
        self.layers = {}
        for layer_elem in root.findall("layer"):
            layer = Layer.from_xml(layer_elem)
            self.layers[layer.name] = layer
        self.objectgroups = {}
        for og_elem in root.findall("objectgroup"):
            og = ObjectGroup.from_xml(og_elem)
            self.objectgroups[og.name] = og
        return self

    def save(self, path: Optional[str] = None, encoding: str = "utf-8", indent: Optional[int] = None) -> None:
        out_path = path or self.path
        if out_path is None:
            raise ValueError("No save path specified")
        root = ET.Element("map", {
            "version": self.version,
            "orientation": self.orientation,
            "renderorder": self.renderorder,
            "width": str(self.width),
            "height": str(self.height),
            "tilewidth": str(self.tilewidth),
            "tileheight": str(self.tileheight),
            "nextobjectid": str(self.nextobjectid)
        })
        if self.properties:
            props_elem = ET.SubElement(root, "properties")
            for prop in self.properties:
                prop.to_xml(props_elem)
        for ts in self.tilesets:
            root.append(ts.to_xml())
        for layer in self.layers.values():
            root.append(layer.to_xml())
        for og in self.objectgroups.values():
            root.append(og.to_xml())
        if indent is not None:
            ET.indent(root, space=" " * indent)
        tree = ET.ElementTree(root)
        tree.write(out_path, encoding=encoding, xml_declaration=True)

    def layer(self, name: str) -> Layer:
        if name not in self.layers:
            raise KeyError(f"Layer '{name}' not found")
        return self.layers[name]

    def objectgroup(self, name: str) -> ObjectGroup:
        if name not in self.objectgroups:
            raise KeyError(f"ObjectGroup '{name}' not found")
        return self.objectgroups[name]

    def add_objectgroup(self, group: ObjectGroup) -> None:
        self.objectgroups[group.name] = group

    def remove_objectgroup(self, name: str) -> None:
        self.objectgroups.pop(name, None)

    def get_tileset_by_gid(self, gid: int) -> Optional[Tileset]:
        for ts in self.tilesets:
            if ts.firstgid <= gid < ts.firstgid + ts.tilecount:
                return ts
        return None

    def get_tile_by_gid(self, gid: int) -> Optional[Tile]:
        ts = self.get_tileset_by_gid(gid)
        if ts:
            return ts.get_tile(gid)
        return None

    def allocate_ids(self, count: int = 1) -> List[int]:
        ids = list(range(self.nextobjectid, self.nextobjectid + count))
        self.nextobjectid += count
        return ids

    def allocate_id(self) -> int:
        return self.allocate_ids(1)[0]

    @classmethod
    def create_empty(
        cls,
        width: int = 256,
        height: int = 256,
        tile_size: int = 1,
        layer_names: Optional[List[str]] = None
    ) -> 'Map':
        m = cls()
        m.width = width
        m.height = height
        m.tilewidth = tile_size
        m.tileheight = tile_size
        if layer_names:
            for name in layer_names:
                m.layers[name] = Layer(name, width, height)
        return m
