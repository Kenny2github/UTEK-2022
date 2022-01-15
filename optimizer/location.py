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

    def __repr__(self) -> str:
        return f'{self.pos!s} {self.time_required}'

    def __hash__(self) -> int:
        return hash((self.pos, self.time_required))

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

def aggregate(locations: Iterable[Location]) -> list[Location]:
    """Aggregate locations to remove conflicts."""
    aggregated: dict[Vector, Location] = {}
    for location in locations:
        candidate = aggregated.get(location.pos)
        if candidate is not None:
            if location.time_required > candidate.time_required:
                # overwrite previous location that required shorter time
                aggregated[location.pos] = location
        else:
            # set new location at that position
            aggregated[location.pos] = location
    return list(aggregated.values())
