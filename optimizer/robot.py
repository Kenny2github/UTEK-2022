from dataclasses import dataclass
from typing import Generator
from .vector import Vector

@dataclass
class Robot:
    name: str
    move_efficiency: int
    clean_efficiency: int
    pos: Vector = Vector(0, 0)

    def __str__(self) -> str:
        return f'Robot Name: {self.name}; ' \
            f'Movement Efficiency: {self.move_efficiency}; ' \
            f'Cleaning Efficiency: {self.clean_efficiency};'

    def get_direction(self, from_pos: Vector, to_pos: Vector) -> Vector:
        dv = to_pos - from_pos
        return Vector(
            0 if dv.x == 0 else (
                1 if dv.x > 0 else -1),
            0 if dv.y == 0 else (
                1 if dv.y > 0 else -1)
        )

    def pathfind(self, pos: Vector) -> Generator[Vector, None, None]:
        """Find and yield the shortest path to the position ``pos``."""
        direction = self.get_direction(self.pos, pos)
        current = self.pos
        while current.x != pos.x and current.y != pos.y:
            yield current
            current += direction
        yield current
        direction = self.get_direction(current, pos)
        while current != pos:
            current += direction
            yield current
