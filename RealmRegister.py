from dataclasses import dataclass
from realm import Realm

@dataclass
class RealmRegister:
    realms: dict #key: name, value: Realms

    def __init__(self):
        self.realms = dict()
        realm_name1 = "default_realm1"
        realm_name2 = "default_realm2"
        self.realms[realm_name1] = Realm(realm_name1, "this is the first realm", 0, 0, 0)
        self.realms[realm_name2] = Realm(realm_name2, "this is the second realm", 0, 0, 1)

    def AddRealm(self, name, realm):
        self.realms[name] = realm
