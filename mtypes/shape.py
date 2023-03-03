from dataclasses import dataclass


@dataclass(frozen=True)
class Circle:
    x: int
    y: int
    r: int


@dataclass(frozen=True)
class Rect:
    x: int
    y: int
    width: int
    height: int
