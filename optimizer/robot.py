from dataclasses import dataclass
from itertools import permutations
from typing import Iterable
from .location import Location, shortest_path
from .obstacle import Obstacle
from .partitions import partitions
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

    def __repr__(self) -> str:
        return f'({self.name}, move: {self.move_efficiency} clean: {self.clean_efficiency})'

    def __hash__(self) -> int:
        return hash((self.name, self.move_efficiency, self.clean_efficiency))

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

    def visit(self, locations: list[Location],
              obstacles: list[Obstacle] = None,
              do_print: bool = True) -> int:
        cost = 0
        path = shortest_path(tuple(sorted(locations)))
        if do_print:
            print('Robot', self.name)
        # Traverse the path
        for location in path:
            for position in self.pathfind(location.pos, obstacles):
                if do_print:
                    print('move', position)
                cost += self.move_efficiency
            self.pos = location.pos
            if do_print:
                print('clean', location.pos)
            cost += self.clean_efficiency * location.time_required
        # return to home
        for position in self.pathfind(Vector(0, 0), obstacles):
            if do_print:
                print('move', position)
            cost += self.move_efficiency
        if do_print:
            print('rest\n')
        self.pos = Vector(0, 0)
        return cost

def optimize(robots: Iterable[Robot], locations: Iterable[Location],
             obstacles: Iterable[Obstacle]) -> dict[Robot, list[Location]]:
    robots = list(robots)
    locations = list(locations)
    results = {}
    best_cost: int = None
    # when there are fewer robots than locations,
    # some robots will be mapped to multiple locations
    for partition in partitions(locations):
        if len(partition) != len(robots):
            continue
        for permo in permutations(robots):
            # when there are fewer locations than robots, some of the robots
            # will go unused, but eventually they will be checked as part of
            # other permutations of this combination
            tmp_results = {robot: part for robot, part in zip(permo, partition)}
            cost = 0
            for robot, path in tmp_results.items():
                cost += robot.visit(path, obstacles, False)
            if best_cost is None or cost < best_cost:
                results = tmp_results
                best_cost = cost
    return results
