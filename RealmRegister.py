from dataclasses import dataclass
from realm import Realm, RealmCoord



@dataclass
class RealmRegister:
    realms: dict #key: name, value: Realms

    def __init__(self):
        self.realms = dict()
        realm_coord1 = RealmCoord(0,0)
        realm_coord2 = RealmCoord(1,0)
        realm_coord3 = RealmCoord(2,0)
        realm_coord4 = RealmCoord(3,0)
        
        self.realms[RealmCoord(0,0)] = Realm("Realm1", "this is the first realm", realm_coord1, "first realm", "easy") #first zero is the mini_adventure ID
        self.realms[RealmCoord(1,0)] = Realm("Realm2", "this is the second realm", realm_coord2, "second realm", "medium")
        self.realms[RealmCoord(2,0)] = Realm("Realm3", "this is the third realm", realm_coord3,  "third realm", "hard")
        self.realms[RealmCoord(3,0)] = Realm("Realm3", "this is the fourth realm", realm_coord4, "fourth realm", "extreme")

    def AddRealm(self, realm_coord, realm):
        self.realms[realm_coord] = realm


