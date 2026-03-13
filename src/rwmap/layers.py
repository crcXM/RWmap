import xml.etree.ElementTree as ET
from typing import List, Optional, Tuple, Iterator
import base64
import gzip
import zlib
import struct

from .properties import Property


class Layer:

    def __init__(
        self,
        name: str,
        width: int,
        height: int,
        data: Optional[List[int]] = None,
        encoding: str = "base64",
        compression: Optional[str] = "gzip",
        opacity: float = 1.0,
        visible: bool = True,
        offsetx: float = 0.0,
        offsety: float = 0.0,
        properties: Optional[List[Property]] = None,
    ):
        self.name = name
        self.width = width
        self.height = height
        self.encoding = encoding
        self.compression = compression
        self.opacity = opacity
        self.visible = visible
        self.offsetx = offsetx
        self.offsety = offsety
        self.properties = properties or []
        self._data = data[:] if data is not None else [0] * (width * height)

    @property
    def data(self) -> List[int]:
        return self._data

    def __getitem__(self, key: Tuple[int, int]) -> int:
        x, y = key
        if not (0 <= x < self.width and 0 <= y < self.height):
            raise IndexError(f"坐标 ({x}, {y}) 超出范围")
        return self._data[y * self.width + x]

    def __setitem__(self, key: Tuple[int, int], value: int) -> None:
        x, y = key
        if not (0 <= x < self.width and 0 <= y < self.height):
            raise IndexError(f"坐标 ({x}, {y}) 超出范围")
        self._data[y * self.width + x] = value

    def __iter__(self) -> Iterator[Tuple[int, int, int]]:
        for y in range(self.height):
            for x in range(self.width):
                yield x, y, self._data[y * self.width + x]

    def fill(self, tile_id: int) -> None:
        self._data = [tile_id] * (self.width * self.height)

    def reencode(self, encoding: str, compression: Optional[str] = None) -> 'Layer':
        self.encoding = encoding
        self.compression = compression
        return self

    def encode_data(self) -> bytes:
        packed = b"".join(struct.pack('i', n) for n in self._data)
        if self.compression == "gzip":
            packed = gzip.compress(packed)
        elif self.compression == "zlib":
            packed = zlib.compress(packed)
        return packed

    def decode_data(self, data: bytes) -> List[int]:
        if self.compression == "gzip":
            data = gzip.decompress(data)
        elif self.compression == "zlib":
            data = zlib.decompress(data)
        fmt = str(self.width * self.height) + 'i'
        return list(struct.unpack(fmt, data))

    @classmethod
    def from_xml(cls, elem: ET.Element) -> 'Layer':
        name = elem.get("name", "")
        width = int(elem.get("width", 0))
        height = int(elem.get("height", 0))
        opacity = float(elem.get("opacity", 1.0))
        visible = elem.get("visible", "1") != "0"
        offsetx = float(elem.get("offsetx", 0))
        offsety = float(elem.get("offsety", 0))
        data_elem = elem.find("data")
        if data_elem is None:
            raise ValueError("Layer missing data element")
        encoding = data_elem.get("encoding", "csv")
        compression = data_elem.get("compression")
        text = data_elem.text or ""
        if encoding == "csv":
            data = [int(x.strip()) for x in text.strip().split(',') if x.strip()]
        elif encoding == "base64":
            raw = base64.b64decode(text)
            if compression == "gzip":
                raw = gzip.decompress(raw)
            elif compression == "zlib":
                raw = zlib.decompress(raw)
            fmt = str(width * height) + 'i'
            data = list(struct.unpack(fmt, raw))
        else:
            raise NotImplementedError(f"Encoding {encoding} not supported")
        props = []
        props_elem = elem.find("properties")
        if props_elem is not None:
            for prop_elem in props_elem.findall("property"):
                props.append(Property.from_xml(prop_elem))
        return cls(name, width, height, data, encoding, compression,
                   opacity, visible, offsetx, offsety, props)

    def to_xml(self) -> ET.Element:
        attrs = {"name": self.name, "width": str(self.width), "height": str(self.height)}
        if self.opacity != 1.0:
            attrs["opacity"] = str(self.opacity)
        if not self.visible:
            attrs["visible"] = "0"
        if self.offsetx != 0:
            attrs["offsetx"] = str(self.offsetx)
        if self.offsety != 0:
            attrs["offsety"] = str(self.offsety)
        elem = ET.Element("layer", attrs)
        if self.properties:
            props_elem = ET.SubElement(elem, "properties")
            for prop in self.properties:
                prop.to_xml(props_elem)
        data_elem = ET.SubElement(elem, "data", {"encoding": self.encoding})
        if self.compression:
            data_elem.set("compression", self.compression)
        data_elem.text = base64.b64encode(self.encode_data()).decode()
        return elem
