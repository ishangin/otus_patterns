from dataclasses import dataclass

__all__ = ['Vector']


@dataclass
class Vector:
    """
    type Vector(x, y)
    """
    x: float
    y: float

    def add(self, vec: "Vector") -> "Vector":
        return Vector(self.x + vec.x, self.y + vec.y)
