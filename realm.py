from dataclasses import dataclass
import uuid



@dataclass(frozen=True)
class RealmCoord:
    x: int
    y: int

    # def __init__(self, x, y):
    #     self.x = x
    #     self.y = y



@dataclass
class Realm:
    realm_id: str
    name: str
    Coord: RealmCoord 
    description: str = ""
    miniAdventure_menuID: str = ""#miniAdventure Menu should have an ID.
    

    # map_id: int = 0
    # x_coord: int = 0 #not sure if these coordinates are required or needed. might need?
    # y_coord: int = 0 #not sure if these coordinates are required or needed. might need?
    
    def __init__(self, name, description, RealmCoord, miniAdventure_menuID):
        self.realm_id = uuid.uuid4() #generates a unique ID
        self.name = name
        self.description = description
        self.miniAdventure_menuID = miniAdventure_menuID
        self.Coord= RealmCoord
    

