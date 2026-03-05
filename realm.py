from dataclasses import dataclass

@dataclass
class Realm:
    realm_id: str
    name: str
    description: str = ""
    trigger_adventureID: str #should use miniAdventure.id to identify which adventure to trigger.
    # map_id: int = 0
    x_coord: int = 0 #not sure if these coordinates are required or needed. might need?
    y_coord: int = 0 #not sure if these coordinates are required or needed. might need?
    