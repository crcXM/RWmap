from typing import List, Optional, Union, Any

from ..properties import Property
from ..objects import Shape, Object
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
