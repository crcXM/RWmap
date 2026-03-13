import xml.etree.ElementTree as ET
from typing import List, Optional, Union, Any

from ..properties import Property
from ..objects import Shape, Object, ObjectGroup
from .units import UnitSpec


class Trigger(Object):

    def __init__(
        self,
        name: str = "",
        type: str = "",
        x: float = 0,
        y: float = 0,
        width: float = 20,
        height: float = 20,
        rotation: float = 0,
        visible: bool = True,
        shape: Optional[Shape] = None,
        gid: Optional[int] = None,
        text: Optional[str] = None,
        properties: Optional[List[Property]] = None,
        id: Optional[int] = None,
    ):
        super().__init__(name, type, x, y, width, height, rotation, visible,
                         shape, gid, text, properties, id)

    def set(self, **kwargs: Any) -> 'Trigger':
        super().set(**kwargs)
        return self

    def spawn(self, units_spec: Union[str, UnitSpec]) -> 'Trigger':
        if isinstance(units_spec, UnitSpec):
            return self.set(spawnUnits=str(units_spec))
        return self.set(spawnUnits=units_spec)

    def activate_by(self, *ids: str) -> 'Trigger':
        return self.set(activatedBy=','.join(ids))

    def deactivate_by(self, *ids: str) -> 'Trigger':
        return self.set(deactivatedBy=','.join(ids))

    def also_activate(self, *ids: str) -> 'Trigger':
        return self.set(alsoActivate=','.join(ids))

    def delay(self, time: str) -> 'Trigger':
        return self.set(delay=time)

    def warmup(self, time: str) -> 'Trigger':
        return self.set(warmup=time)

    def repeat(self, time: str) -> 'Trigger':
        return self.set(repeatDelay=time)

    def reset_after(self, time: str) -> 'Trigger':
        return self.set(resetActivationAfter=time)

    def team(self, t: int) -> 'Trigger':
        return self.set(team=t)

    def comment(self, text: str) -> 'Trigger':
        return self.set(comment=text)

    def all_to_activate(self, value: bool) -> 'Trigger':
        return self.set(allToActivate=value)


class TriggerLayer(ObjectGroup):

    def __init__(
        self,
        triggers: Optional[List[Trigger]] = None,
        color: Optional[str] = None,
        opacity: float = 1.0,
        visible: bool = True,
        offsetx: float = 0.0,
        offsety: float = 0.0,
        properties: Optional[List[Property]] = None,
    ):
        super().__init__(
            name="Triggers",
            objects=triggers if triggers is not None else [],# type: ignore
            color=color,
            opacity=opacity,
            visible=visible,
            offsetx=offsetx,
            offsety=offsety,
            properties=properties,
        )

    def add(self, trigger: Trigger) -> 'TriggerLayer':# type: ignore
        super().add(trigger)
        return self

    def extend(self, triggers: List[Trigger]) -> 'TriggerLayer':# type: ignore
        super().extend(triggers)# type: ignore
        return self

    @property
    def triggers(self) -> List[Trigger]:
        return self.objects  # type: ignore

    @classmethod
    def from_xml(cls, elem: ET.Element) -> 'TriggerLayer':
        og = ObjectGroup.from_xml(elem)
        return cls(
            triggers=og.objects,  # type: ignore
            color=og.color,
            opacity=og.opacity,
            visible=og.visible,
            offsetx=og.offsetx,
            offsety=og.offsety,
            properties=og.properties,
        )
