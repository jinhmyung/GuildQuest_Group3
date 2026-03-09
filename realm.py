from dataclasses import dataclass
import uuid

@dataclass
class Realm:
    realm_id: str
    name: str
    description: str = ""
    miniAdventure_menuID: str = ""#miniAdventure Menu should have an ID.

    # map_id: int = 0
    x_coord: int = 0 #not sure if these coordinates are required or needed. might need?
    y_coord: int = 0 #not sure if these coordinates are required or needed. might need?
    
    def __init__(self, name, description, miniAdventure_menuID, x_coord, y_coord):
        self.realm_id = uuid.uuid4() #generates a unique ID
        self.name = name
        self.description = description
        self.miniAdventure_menuID = miniAdventure_menuID
        self.x_coord = x_coord
        self.y_coord = y_coord
    