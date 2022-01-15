from __future__ import annotations
from dataclasses import dataclass

@dataclass
class Vector:
    x: int
    y: int

    @property
    def pos(self) -> tuple[int, int]:
        return (self.x, self.y)

    @pos.setter
    def pos(self, value: tuple[int, int]):
        self.x, self.y = value

    def __str__(self) -> str:
        return f'{self.x} {self.y}'

    def __hash__(self) -> int:
        return hash(self.pos)

    def __add__(self, other: Vector) -> Vector:
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Vector) -> Vector:
        return self + (-other)

    def __mul__(self, other: int) -> Vector:
        return Vector(self.x * other, self.y * other)

    __rmul__ = __mul__

    def __floordiv__(self, other: int) -> Vector:
        return Vector(self.x // other, self.y // other)

    def __neg__(self) -> Vector:
        return self * -1

    def __abs__(self) -> int:
        return max(abs(self.x), abs(self.y))

    def distance_to(self, other: Vector) -> int:
        return abs(other - self)