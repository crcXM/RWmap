from typing import cast

from .triggers import Trigger
from ..objects import Object, ObjectGroup
from ..layers import Layer
from ..maps import Map


class RwMap(Map):

    def __init__(self, path: str | None = None) -> None:
        super().__init__(path=path)

    @property
    def triggers(self) -> list[Trigger]:
        og = self.get_objectgroup("Triggers")
        if og is None:
            og = ObjectGroup(name="Triggers", objects=[])
            self.objectgroups.append(og)
        return cast(list[Trigger], og.objects)

    @triggers.setter
    def triggers(self, triggers: list[Trigger]) -> None:
        og = self.get_objectgroup("Triggers")
        if og is None:
            og = ObjectGroup(
                name="Triggers",
                objects=cast(list[Object], triggers),
                color=None,
                opacity=1.0,
                visible=True,
                offsetx=0.0,
                offsety=0.0,
                properties={},
            )
            self.objectgroups.append(og)
        else:
            og.objects = cast(list[Object], triggers)

    @property
    def ground(self) -> Layer | None:
        return self.get_layer("Ground")

    @property
    def items(self) -> Layer | None:
        return self.get_layer("Items")

    @property
    def units(self) -> Layer | None:
        return self.get_layer("Units")

    @classmethod
    def create_empty(
        cls,
        width: int = 256,
        height: int = 256,
        tile_size: int = 20,
        layer_names: list[str] | None = None,
    ) -> "RwMap":
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
