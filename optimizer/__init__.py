import sys
from .obstacle import Obstacle
from .vector import Vector
from .location import Location, shortest_path
from .robot import Robot

def read_info():
    robotc, locationc, obstaclec = map(int, input().split())

    robots: list[Robot] = []
    for _ in range(robotc):
        name, move, clean = input().split()
        robots.append(Robot(name, int(move), int(clean)))

    locations: list[Location] = []
    for _ in range(locationc):
        x, y, time = map(int, input().split())
        locations.append(Location(Vector(x, y), time))

    obstacles: list[Obstacle] = []
    for _ in range(obstaclec):
        x1, y1, x2, y2 = map(int, input().split())
        obstacles.append(Obstacle(Vector(x1, y1), Vector(x2, y2)))

    return robots, locations, obstacles

def run1():
    robots, locations, _ = read_info()
    print('\n'.join(map(str, robots)))
    aggregated: dict[Vector, Location] = {}
    for location in locations:
        candidate = aggregated.get(location.pos)
        if candidate is not None:
            if location.time_required > candidate:
                # overwrite previous location that required shorter time
                aggregated[location.pos] = location
        else:
            # set new location at that position
            aggregated[location.pos] = location
    for i, location in enumerate(aggregated.values(), start=1):
        print(f'Location Number: {i}; {location!s}')

def run2():
    [robot], locations, obstacles = read_info()
    path = shortest_path(locations)
    cost = 0
    print('Robot', robot.name)
    # Traverse the path
    for location in path:
        for position in robot.pathfind(location.pos, obstacles):
            print('move', position)
            cost += robot.move_efficiency
        robot.pos = location.pos
        print('clean', location.pos)
        cost += robot.clean_efficiency * location.time_required
    # return to home
    for position in robot.pathfind(Vector(0, 0), obstacles):
        print('move', position)
        cost += robot.move_efficiency
    print('rest')
    print(cost, file=sys.stderr)

run3 = run2

def run4():
    pass

def run5():
    pass

