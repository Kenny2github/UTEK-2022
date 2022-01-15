from dataclasses import dataclass
from .vector import Vector

@dataclass
class Location:
    pos: Vector
    time_required: int

    def __str__(self) -> str:
        return f'Time required: {self.time_required}; Location: {self.pos!s};'
