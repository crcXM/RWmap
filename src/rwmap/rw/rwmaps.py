from typing import List, Optional, cast

from .triggers import Trigger
from ..objects import Object, ObjectGroup
from ..layers import Layer
from ..maps import Map


class RwMap(Map):

    def __init__(self, path: Optional[str] = None) -> None:
        super().__init__(path=path)

    # ---------- 触发器图层 ----------
    @property
    def triggers(self) -> List[Trigger]:
        og = self.objectgroup("Triggers")
        if og is None:
            # 自动创建空的 Triggers 图层并添加到地图
            og = ObjectGroup(name="Triggers", objects=[])
            self.objectgroups.append(og)
        return cast(List[Trigger], og.objects)

    @triggers.setter
    def triggers(self, triggers: List[Trigger]) -> None:
        og = self.objectgroup("Triggers")
        if og is None:
            og = ObjectGroup(
                name="Triggers",
                objects=cast(List[Object], triggers),
                color=None,
                opacity=1.0,
                visible=True,
                offsetx=0.0,
                offsety=0.0,
                properties=None,
            )
            self.objectgroups.append(og)
        else:
            og.objects = cast(List[Object], triggers)

    @property
    def ground(self) -> Optional[Layer]:
        return self.layer("Ground")

    @property
    def items(self) -> Optional[Layer]:
        return self.layer("Items")

    @property
    def units(self) -> Optional[Layer]:
        return self.layer("Units")

    @classmethod
    def create_empty(
        cls,
        width: int = 256,
        height: int = 256,
        tile_size: int = 20,
        layer_names: Optional[List[str]] = None,
    ) -> "RwMap":
        """创建一个空地图，包含指定的图层和默认的 Triggers 图层。"""
        if layer_names is None:
            layer_names = ["Ground", "Items", "Units", "Set"]

        m = cls()
        m.width = width
        m.height = height
        m.tilewidth = tile_size
        m.tileheight = tile_size

        for name in layer_names:
            m.layers.append(Layer(name=name, width=width, height=height))

        _ = m.triggers

        return m
