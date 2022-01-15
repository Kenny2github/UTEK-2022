from functools import partial
from typing import Iterable
from itertools import permutations
from dataclasses import dataclass
from multiprocessing import Process, Queue
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


def shortest_path_guaranteed(locations: Iterable[Location], q: Queue):
    """Find the shortest path between all the locations.

    ...by checking every single possible path.
    This is guaranteed to find the shortest path, but may
    take unreasonably long for large input, since it runs in O(n!) time.
    It returns the answer into an argument, for use with multiprocessing.
    """
    q.put(min(permutations(locations), key=path_cost))

def shortest_path_heuristic(locations: Iterable[Location]) -> tuple[Location]:
    """Find the shortest path between all the locations.

    ...by assuming that sorting them by coordinates is optimal.
    This will probably be okayish but nowhere near the best.
    """
    return tuple(sorted(locations, key=lambda loc: loc.pos.pos))

def shortest_path(locations: Iterable[Location]) -> tuple[Location]:
    """Find the shortest path between all the locations.

    This will try a brute force method, or use a best guess if that
    takes too long.
    """
    q = Queue()
    p = Process(target=partial(shortest_path_guaranteed, locations, q))
    p.start()

    # wait 20 seconds for the process to finish
    p.join(20)

    if p.is_alive(): # 20 seconds have passed
        p.terminate() # give up
        p.join()
        return shortest_path_heuristic(locations)
    return q.get_nowait()

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
