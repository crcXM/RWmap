from typing import Dict, Optional, Union, Any


class UnitSpec:

    def __init__(self, name: str):
        self.name: str = name
        self.attrs: Dict[str, Optional[Union[bool, int, float, str]]] = {}
        self._count: int = 1

    @property
    def count(self) -> int:
        return self._count

    def falling(self) -> 'UnitSpec':
        self.attrs['falling'] = True
        return self

    def grid_align(self) -> 'UnitSpec':
        self.attrs['gridAlign'] = True
        return self

    def spawn_chance(self, value: float) -> 'UnitSpec':
        self.attrs['spawnChance'] = value
        return self

    def tech_level(self, value: int) -> 'UnitSpec':
        self.attrs['techLevel'] = value
        return self

    def offset_x(self, value: float) -> 'UnitSpec':
        self.attrs['offsetX'] = value
        return self

    def offset_y(self, value: float) -> 'UnitSpec':
        self.attrs['offsetY'] = value
        return self

    def offset_random_xy(self, value: float) -> 'UnitSpec':
        self.attrs['offsetRandomXY'] = value
        return self

    def offset_random_x(self, value: float) -> 'UnitSpec':
        self.attrs['offsetRandomX'] = value
        return self

    def offset_random_y(self, value: float) -> 'UnitSpec':
        self.attrs['offsetRandomY'] = value
        return self

    def offset_height(self, value: float) -> 'UnitSpec':
        self.attrs['offsetHeight'] = value
        return self

    def offset_random_dir(self, value: float) -> 'UnitSpec':
        self.attrs['offsetRandomDir'] = value
        return self

    def offset_dir(self, value: float) -> 'UnitSpec':
        self.attrs['offsetDir'] = value
        return self

    def max_spawn_limit(self, value: int) -> 'UnitSpec':
        self.attrs['maxSpawnLimit'] = value
        return self

    def __str__(self) -> str:
        base = self.name
        if self.attrs:
            items = []
            for k, v in self.attrs.items():
                if isinstance(v, bool):
                    items.append(f"{k}={str(v).lower()}")
                else:
                    items.append(f"{k}={v}")
            base = f"{self.name}({','.join(items)})"
        if self._count > 1:
            return f"{base}*{self._count}"
        return base

    def __repr__(self) -> str:
        return str(self)

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, UnitSpec):
            return str(self) == str(other)
        return str(self) == str(other)

    def __mul__(self, count: int) -> 'UnitSpec':
        new_spec = UnitSpec(self.name)
        new_spec.attrs = self.attrs.copy()
        new_spec._count = count
        return new_spec


def unit(name: str) -> UnitSpec:
    return UnitSpec(name)
