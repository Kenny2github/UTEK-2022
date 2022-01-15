import sys
from .obstacle import Obstacle
from .vector import Vector
from .location import Location, aggregate
from .robot import Robot, optimize

sys.setrecursionlimit(10000)

def read_info() -> tuple[list[Robot], list[Location], list[Obstacle]]:
    robotc, locationc, obstaclec = map(int, input().split())

    robots: list[Robot] = []
    for _ in range(robotc):
        name, move, clean = input().split()
        robots.append(Robot(name, int(move), int(clean)))

    locations: list[Location] = []
    for _ in range(locationc):
        x, y, time = map(int, input().split())
        locations.append(Location(Vector(x, y), time))
    locations = aggregate(locations)

    obstacles: list[Obstacle] = []
    for _ in range(obstaclec):
        x1, y1, x2, y2 = map(int, input().split())
        obstacles.append(Obstacle(Vector(x1, y1), Vector(x2, y2)))

    return robots, locations, obstacles

def run1():
    robots, locations, _ = read_info()
    print('\n'.join(map(str, robots)))
    for i, location in enumerate(locations, start=1):
        print(f'Location Number: {i}; {location!s}')

def run2():
    robots, locations, obstacles = read_info()
    cost = 0
    for robot in robots:
        cost += robot.visit(locations, obstacles)
    print(cost, file=sys.stderr)

run3 = run2

def run4():
    robots, locations, obstacles = read_info()
    cost = 0
    results = optimize(robots, locations, obstacles)
    print(results, file=sys.stderr)
    for robot, path in results.items():
        cost += robot.visit(path, obstacles)
    print(cost, file=sys.stderr)

run5 = run4
