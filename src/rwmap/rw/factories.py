from typing import List, Optional, Union, Tuple

from .triggers import Trigger, Shape
from .units import UnitSpec


def map_info(type: str = "skirmish", fog: str = "none", intro: str = "", **kwargs) -> Trigger:
    obj = Trigger(name="map_info", type="basic")
    obj.set(type=type, fog=fog)
    if intro:
        obj.set(introText=intro)
    for k, v in kwargs.items():
        obj.set(**{k: v})
    return obj


def team_info(
    team: int,
    credits: int = 0,
    allyGroup: int = 0,
    disabledAI: bool = False,
    lockAiDifficulty: Optional[int] = None,
    ai: str = "",
    basicAI: bool = False,
    **kwargs
) -> Trigger:
    obj = Trigger(name=f"team_{team}", type="team_info")
    obj.set(team=team)
    if credits:
        obj.set(credits=credits)
    if allyGroup:
        obj.set(allyGroup=allyGroup)
    if disabledAI:
        obj.set(disabledAI=True)
    if lockAiDifficulty is not None:
        obj.set(lockAiDifficulty=lockAiDifficulty)
    if ai:
        obj.set(ai=ai)
    if basicAI:
        obj.set(basicAI="")
    for k, v in kwargs.items():
        obj.set(**{k: v})
    return obj


def unit_detect(
    x: float, y: float,
    name: Optional[str] = None,
    width: float = 20,
    height: float = 20,
    rotation: float = 0.0,
    shape: Optional[str] = None,
    polygon_points: Optional[List[Tuple[int, int]]] = None,
    minUnits: Optional[int] = None,
    maxUnits: Optional[int] = None,
    unitType: Optional[str] = None,
    **kwargs
) -> Trigger:
    shape_obj: Optional[Shape] = None
    if shape == "point":
        shape_obj = Shape("point")
    elif shape == "ellipse":
        shape_obj = Shape("ellipse")
    elif shape in ("polygon", "polyline") and polygon_points:
        shape_obj = Shape(shape, polygon_points)

    obj = Trigger(
        name=name or f"detect_{x}_{y}",
        type="unitDetect",
        x=x, y=y,
        width=width, height=height,
        rotation=rotation,
        shape=shape_obj
    )
    obj.set(resetActivationAfter="1s")
    if minUnits is not None:
        obj.set(minUnits=minUnits)
    if maxUnits is not None:
        obj.set(maxUnits=maxUnits)
    if unitType is not None:
        obj.set(unitType=unitType)
    for k, v in kwargs.items():
        obj.set(**{k: v})
    return obj


def unit_add(
    x: float, y: float,
    team: int = -1,
    spawnUnits: Optional[Union[str, UnitSpec]] = None,
    name: Optional[str] = None,
    **kwargs
) -> Trigger:
    obj = Trigger(name=name or f"add_{x}_{y}", type="unitAdd", x=x, y=y)
    obj.set(team=team)
    if spawnUnits is not None:
        if isinstance(spawnUnits, UnitSpec):
            obj.set(spawnUnits=str(spawnUnits))
        else:
            obj.set(spawnUnits=spawnUnits)
    for k, v in kwargs.items():
        obj.set(**{k: v})
    return obj


def unit_remove(
    x: float, y: float, width: float, height: float,
    team: int = 0,
    onlyIfEmpty: bool = False,
    name: Optional[str] = None,
    **kwargs
) -> Trigger:
    obj = Trigger(name=name or f"remove_{x}_{y}", type="unitRemove", x=x, y=y, width=width, height=height)
    obj.set(team=team)
    if onlyIfEmpty:
        obj.set(onlyIfEmpty=True)
    for k, v in kwargs.items():
        obj.set(**{k: v})
    return obj


def map_text(
    x: float, y: float,
    text: str,
    color: str = "white",
    size: int = 12,
    name: Optional[str] = None,
    **kwargs
) -> Trigger:
    obj = Trigger(name=name or f"text_{x}_{y}", type="mapText", x=x, y=y)
    obj.set(text=text, textColor=color, textSize=size)
    for k, v in kwargs.items():
        obj.set(**{k: v})
    return obj


def point(
    name: str,
    x: float, y: float,
    **kwargs
) -> Trigger:
    obj = Trigger(name=name, type="point", x=x, y=y)
    for k, v in kwargs.items():
        obj.set(**{k: v})
    return obj


def move(
    x: float, y: float,
    target: str,
    unload: bool = False,
    name: Optional[str] = None,
    **kwargs
) -> Trigger:
    obj = Trigger(name=name or f"move_{x}_{y}", type="move", x=x, y=y)
    obj.set(target=target)
    if unload:
        obj.set(unload="")
    for k, v in kwargs.items():
        obj.set(**{k: v})
    return obj


def rotate(
    x: float, y: float,
    dir: float,
    name: Optional[str] = None,
    **kwargs
) -> Trigger:
    obj = Trigger(name=name or f"rotate_{x}_{y}", type="rotate", x=x, y=y)
    obj.set(dir=dir)
    for k, v in kwargs.items():
        obj.set(**{k: v})
    return obj


def change_credits(
    x: float, y: float,
    team: int,
    add: Optional[int] = None,
    set: Optional[int] = None,
    name: Optional[str] = None,
    **kwargs
) -> Trigger:
    obj = Trigger(name=name or f"credits_{x}_{y}", type="changeCredits", x=x, y=y)
    obj.set(team=team)
    if add is not None:
        obj.set(add=add)
    if set is not None:
        obj.set(set=set)
    for k, v in kwargs.items():
        obj.set(**{k: v})
    return obj


def basic(
    x: float, y: float,
    name: Optional[str] = None,
    **kwargs
) -> Trigger:
    obj = Trigger(name=name or f"basic_{x}_{y}", type="basic", x=x, y=y)
    for k, v in kwargs.items():
        obj.set(**{k: v})
    return obj


def objective(
    x: float, y: float,
    name: str = "objective",
    **kwargs
) -> Trigger:
    obj = Trigger(name=name, type="objective", x=x, y=y)
    for k, v in kwargs.items():
        obj.set(**{k: v})
    return obj


def camera_start(
    x: float, y: float,
    zoomTo: Optional[int] = None,
    name: Optional[str] = None,
    **kwargs
) -> Trigger:
    obj = Trigger(name=name or "camera_start", type="camera_start", x=x, y=y)
    if zoomTo:
        obj.set(zoomTo=zoomTo)
    for k, v in kwargs.items():
        obj.set(**{k: v})
    return obj


def fall(
    x: float, y: float,
    width: float = 20,
    height: float = 20,
    name: Optional[str] = None,
    **kwargs
) -> Trigger:
    obj = Trigger(name=name or f"fall_{x}_{y}", type="fall", x=x, y=y, width=width, height=height)
    for k, v in kwargs.items():
        obj.set(**{k: v})
    return obj


def set_team(
    x: float, y: float,
    width: float, height: float,
    team: int,
    name: Optional[str] = None,
    **kwargs
) -> Trigger:
    obj = Trigger(name=name or f"set_team_{x}_{y}", type="set_team", x=x, y=y, width=width, height=height)
    obj.set(team=team)
    for k, v in kwargs.items():
        obj.set(**{k: v})
    return obj


def ai_allow_full_use(
    x: float, y: float,
    width: float, height: float,
    name: Optional[str] = None,
    **kwargs
) -> Trigger:
    obj = Trigger(name=name or f"ai_{x}_{y}", type="ai_allow_full_use", x=x, y=y, width=width, height=height)
    for k, v in kwargs.items():
        obj.set(**{k: v})
    return obj


def unit_info(
    x: float, y: float,
    unit: Union[str, UnitSpec],
    team: int = -1,
    name: Optional[str] = None,
    **kwargs
) -> Trigger:
    unit_str = str(unit) if isinstance(unit, UnitSpec) else unit
    obj = Trigger(name=name or f"unit_{x}_{y}", type="info", x=x, y=y)
    obj.set(unit=unit_str, team=team)
    for k, v in kwargs.items():
        obj.set(**{k: v})
    return obj


