from dataclasses import dataclass
from .vector import Vector

@dataclass
class Obstacle:
    bottomleft: Vector
    topright: Vector

    def intersects(self, point: Vector) -> bool:
        return (self.bottomleft.x <= point.x <= self.topright.x
                and self.bottomleft.y <= point.y <= self.topright.y)