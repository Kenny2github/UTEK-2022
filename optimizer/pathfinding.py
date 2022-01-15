"""A* search algorithm."""
from __future__ import annotations
from math import hypot
from dataclasses import dataclass
from functools import total_ordering
from typing import Iterable, Optional
from heapq import *
from .vector import Vector

@dataclass
@total_ordering
class Node:
    pos: Vector
    dest: Vector
    path_length: int
    prev: Optional[Node] = None

    @property
    def heuristic(self) -> float:
        return self.path_length + hypot(self.pos.x - self.dest.x,
                                        self.pos.y - self.dest.y)

    def __eq__(self, other: Node) -> bool:
        return self.heuristic == other.heuristic

    def __lt__(self, other: Node) -> bool:
        return self.heuristic < other.heuristic

DIRECTIONS = {Vector(x, y) for x in {-1, 0, 1} for y in {-1, 0, 1}}
DIRECTIONS.discard(Vector(0, 0))

def pathfind(from_pos: Vector, to_pos: Vector, excluded: Iterable[Vector]
             ) -> list[Vector]:
    end = expand(Node(from_pos, to_pos, 0), to_pos, [], set(excluded))
    path = [end.pos]
    while end.prev is not None:
        end = end.prev
        path.append(end.pos)
    path.reverse()
    return path

def expand(node: Node, dest: Vector, queue: list[Node],
           excluded: set[Vector]) -> list[Node]:
    if node.pos == dest:
        return node
    for direction in DIRECTIONS:
        if direction in excluded:
            continue # do not expand this node
        heappush(queue, Node(node.pos + direction, dest,
                             node.path_length + 1, node))
    return expand(heappop(queue), dest, queue, excluded)