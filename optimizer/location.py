from typing import Iterable
from itertools import permutations
from dataclasses import dataclass
from .vector import Vector

@dataclass
class Location:
    pos: Vector
    time_required: int

    def __str__(self) -> str:
        return f'Time required: {self.time_required}; Location: {self.pos!s};'

def path_cost(path: Iterable[Location]) -> int:
    """Find the base cost of a path.

    Multiply by movement efficiency as needed.
    """
    cost = 0
    last: Vector = Vector(0, 0)
    for location in path:
        cost += last.distance_to(location.pos)
        last = location.pos
    cost += last.distance_to(Vector(0, 0))
    return cost

def shortest_path(locations: Iterable[Location]) -> tuple[Location]:
    """Find the shortest path between all the locations

    ...by checking every single possible path.
    """
    return min(permutations(locations), key=path_cost)
