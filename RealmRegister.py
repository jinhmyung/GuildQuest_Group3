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
        
        self.realms[RealmCoord(0,0)] = Realm("Grassfield", realm_coord1, "calm grassy lands", "easy") #first zero is the mini_adventure ID
        self.realms[RealmCoord(1,0)] = Realm("Rockfield Deserts", realm_coord2, "barren land", "medium")
        self.realms[RealmCoord(2,0)] = Realm("IcePeak Summit", realm_coord3,  "treacherous mountains", "hard")
        self.realms[RealmCoord(3,0)] = Realm("Galactic Zone", realm_coord4, "outer space", "extreme")

    def AddRealm(self, realm_coord, realm):
        self.realms[realm_coord] = realm


