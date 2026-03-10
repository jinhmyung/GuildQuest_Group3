from dataclasses import dataclass
from realm import Realm, RealmCoord



@dataclass
class RealmRegister:
    realms: dict #key: name, value: Realms

    def __init__(self):
        self.realms = dict()
        realm_coord1 = RealmCoord(0,0)
        realm_coord2 = RealmCoord(1,0)
        
        self.realms[RealmCoord(0,0)] = Realm("Realm1", "this is the first realm", realm_coord1, 0) #first zero is the mini_adventure ID
        self.realms[RealmCoord(1,0)] = Realm("Realm2", "this is the second realm", realm_coord2,  1)

    def AddRealm(self, realm_coord, realm):
        self.realms[realm_coord] = realm


