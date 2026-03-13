from typing import List, Optional

from .triggers import TriggerLayer
from ..layers import Layer
from ..maps import Map


class RwMap(Map):

    def __init__(self, path: Optional[str] = None):
        super().__init__(path)
        self._triggers: Optional[TriggerLayer] = None
        if "Triggers" in self.objectgroups:
            og = self.objectgroups["Triggers"]
            if isinstance(og, TriggerLayer):
                self._triggers = og
            else:
                self._triggers = TriggerLayer(
                    triggers=og.objects,  # type: ignore
                    color=og.color,
                    opacity=og.opacity,
                    visible=og.visible,
                    offsetx=og.offsetx,
                    offsety=og.offsety,
                    properties=og.properties,
                )
                self.objectgroups["Triggers"] = self._triggers

    @property
    def triggers(self) -> TriggerLayer:
        if self._triggers is None:
            self._triggers = TriggerLayer()
            self.objectgroups["Triggers"] = self._triggers
        return self._triggers

    @triggers.setter
    def triggers(self, layer: TriggerLayer) -> None:
        self._triggers = layer
        self.objectgroups["Triggers"] = layer

    @property
    def ground(self) -> Optional[Layer]:
        return self.layers.get("Ground")

    @property
    def items(self) -> Optional[Layer]:
        return self.layers.get("Items")

    @property
    def units(self) -> Optional[Layer]:
        return self.layers.get("Units")

    @property
    def set_layer(self) -> Optional[Layer]:
        return self.layers.get("Set")

    @classmethod
    def create_empty(
        cls,
        width: int = 256,
        height: int = 256,
        tile_size: int = 20,
        layer_names: Optional[List[str]] = None
    ) -> 'RwMap':
        if layer_names is None:
            layer_names = ["Ground", "Items", "Units", "Set"]
        m = cls()
        m.width = width
        m.height = height
        m.tilewidth = tile_size
        m.tileheight = tile_size
        for name in layer_names:
            m.layers[name] = Layer(name, width, height)
        _ = m.triggers  # 触发自动创建
        return m


