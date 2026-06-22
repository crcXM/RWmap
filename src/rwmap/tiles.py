import xml.etree.ElementTree as ET
from typing import Any

from .properties import properties_from_xml, properties_to_xml


class Tile:

    def __init__(
        self,
        id: int,
        properties: dict[str, Any] = {},
        terrain: str | None = None,
        probability: float | None = None,
        image: str | None = None,
        image_width: int | None = None,
        image_height: int | None = None,
        image_trans: str | None = None,
    ):
        self.id = id
        self.properties = properties.copy()
        self.terrain = terrain
        self.probability = probability
        self.image = image
        self.image_width = image_width
        self.image_height = image_height
        self.image_trans = image_trans

    @classmethod
    def from_xml(cls, elem: ET.Element) -> 'Tile':
        tile_id = int(elem.get("id", 0))
        tile = cls(id=tile_id)
        tile.properties = properties_from_xml(elem.find("properties"))
        tile.terrain = elem.get("terrain")
        prob = elem.get("probability")
        if prob:
            tile.probability = float(prob)
        img_elem = elem.find("image")
        if img_elem is not None:
            tile.image = img_elem.get("source")
            tile.image_width = int(img_elem.get("width", 0)) if img_elem.get("width") else None
            tile.image_height = int(img_elem.get("height", 0)) if img_elem.get("height") else None
            tile.image_trans = img_elem.get("trans")
        return tile

    def to_xml(self) -> ET.Element:
        attrs = {"id": str(self.id)}
        if self.terrain is not None:
            attrs["terrain"] = self.terrain
        if self.probability is not None:
            attrs["probability"] = str(self.probability)
        elem = ET.Element("tile", attrs)
        if self.properties:
            elem.append(properties_to_xml(self.properties))
        if self.image:
            img_attrs = {"source": self.image}
            if self.image_width:
                img_attrs["width"] = str(self.image_width)
            if self.image_height:
                img_attrs["height"] = str(self.image_height)
            if self.image_trans:
                img_attrs["trans"] = self.image_trans
            ET.SubElement(elem, "image", img_attrs)
        return elem


class Tileset:

    def __init__(
        self,
        firstgid: int,
        name: str = "",
        tilewidth: int = 1,
        tileheight: int = 1,
        tilecount: int = 0,
        columns: int = 0,
        source: str | None = None,
        image: str | None = None,
        image_width: int | None = None,
        image_height: int | None = None,
        image_trans: str | None = None,
        is_image_collection: bool = False,
        properties: dict[str, Any] = {},
    ):
        self.firstgid = firstgid
        self.name = name
        self.tilewidth = tilewidth
        self.tileheight = tileheight
        self.tilecount = tilecount
        self.columns = columns
        self.source = source
        self.image = image
        self.image_width = image_width
        self.image_height = image_height
        self.image_trans = image_trans
        self.is_image_collection = is_image_collection
        self.properties = properties.copy()
        self.tiles: dict[int, Tile] = {}

    def add_tile(self, tile: Tile) -> 'Tileset':
        self.tiles[tile.id] = tile
        return self

    def get_tile(self, gid: int) -> Tile | None:
        local_id = gid - self.firstgid
        return self.tiles.get(local_id)

    @classmethod
    def from_xml(cls, elem: ET.Element) -> 'Tileset':
        ts = cls(
            firstgid=int(elem.get("firstgid", 1)),
            name=elem.get("name", ""),
            tilewidth=int(elem.get("tilewidth", 1)),
            tileheight=int(elem.get("tileheight", 1)),
            tilecount=int(elem.get("tilecount", 0)),
            columns=int(elem.get("columns", 0)),
            source=elem.get("source"),
        )
        if ts.source:
            return ts
        img_elem = elem.find("image")
        if img_elem is not None:
            ts.image = img_elem.get("source")
            ts.image_width = int(img_elem.get("width", 0)) if img_elem.get("width") else None
            ts.image_height = int(img_elem.get("height", 0)) if img_elem.get("height") else None
            ts.image_trans = img_elem.get("trans")
        ts.properties = properties_from_xml(elem.find("properties"))
        has_tiles_with_images = False
        for tile_elem in elem.findall("tile"):
            tile = Tile.from_xml(tile_elem)
            if tile.image is not None:
                has_tiles_with_images = True
            ts.tiles[tile.id] = tile
        if has_tiles_with_images and ts.image is None:
            ts.is_image_collection = True
        return ts

    def to_xml(self) -> ET.Element:
        if self.source:
            return ET.Element("tileset", {"firstgid": str(self.firstgid), "source": self.source})
        attrs = {
            "firstgid": str(self.firstgid),
            "name": self.name,
            "tilewidth": str(self.tilewidth),
            "tileheight": str(self.tileheight)
        }
        if self.tilecount:
            attrs["tilecount"] = str(self.tilecount)
        if self.columns:
            attrs["columns"] = str(self.columns)
        elem = ET.Element("tileset", attrs)
        if self.properties:
            elem.append(properties_to_xml(self.properties))
        if self.image and not self.is_image_collection:
            img_attrs = {"source": self.image}
            if self.image_width:
                img_attrs["width"] = str(self.image_width)
            if self.image_height:
                img_attrs["height"] = str(self.image_height)
            if self.image_trans:
                img_attrs["trans"] = self.image_trans
            ET.SubElement(elem, "image", img_attrs)
        for tile in self.tiles.values():
            elem.append(tile.to_xml())
        return elem
