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
    realm_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    Coord: "RealmCoord" = None
    description: str = ""
    miniAdventure_menuID: str = ""
    difficulty = random.choice(["easy", "medium", "hard", "extreme"])

