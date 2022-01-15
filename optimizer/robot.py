from dataclasses import dataclass
from typing import Generator, Iterable
from .obstacle import Obstacle
from .pathfinding import pathfind as _pathfind
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

    def pathfind(self, pos: Vector, around: Iterable[Obstacle] = None
                 ) -> Iterable[Vector]:
        """Find and yield the shortest path to the position ``pos``."""
        excluded = set()
        for obstacle in around or set():
            for x in range(obstacle.bottomleft.x, obstacle.topright.x + 1):
                for y in range(obstacle.bottomleft.y, obstacle.topright.y + 1):
                    excluded.add(Vector(x, y))
        # don't include the starting position
        return _pathfind(self.pos, pos, excluded)[1:]
