from dataclasses import dataclass, field
import random
import uuid



@dataclass(frozen=True)
class RealmCoord:
    x: int
    y: int

    # def __init__(self, x, y):
    #     self.x = x
    #     self.y = y



@dataclass(frozen=True)
class Realm:
    name: str = ""
    Coord: "RealmCoord" = None
    description: str = ""
    difficulty: str = ""

