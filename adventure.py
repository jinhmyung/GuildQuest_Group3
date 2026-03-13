from typing import List
from typing import Type
from typing import Optional
from miniAdventure import MiniAdventure
from mobhunt import MobHunt
from treasureTrap import TreasureTrapAdventure
from dataclasses import dataclass, field
from realm import Realm

class AdventureFactory():
    def __init__(self):
        self.registry = {"Mob Hunt": MobHunt, "Treasure Trap": TreasureTrapAdventure} 
        self.adventureName = ""
        self.adventureID = 0
    
    def getName(self):
        return self.adventureName

    def register(self, name: str, cls: Type[MiniAdventure]):
        self.registry[name] = cls

    def create(self, name: str, *args) -> Optional[MiniAdventure]:
        if name in self.registry:
            return self.registry[name](*args)
        return None
    
    def list_adventures(self) -> List[str]:
        return list(self.registry.keys())

class AdventureMenu():

    instance  = None            #re-used code from Nicol app.py singlton
    
    def __new__(cls):                   
        if cls.instance is None:        
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self):
        if not hasattr(self, "_initalized"):
            self._initialized = True        #end of code reuse.

        self.factory = AdventureFactory()

    def show_options(self):
        return self.factory.list_adventures()
            
    # this one will make an instance of the chosen mini game and start the mini game by calling start_adventure()
    def get_selections(self, choice, *args):
    # the args are player1 player2 and gameID not sure what that does. 
        self.factory.create(choice, *args).start_adventure()

@dataclass
class DictOfAdventureMenu:
    AM_dictionary: dict[Realm, "AdventureMenu"] = field(default_factory=dict)

    def add_menu(self, realm: Realm, menu: "AdventureMenu"):
        self.AM_dictionary[realm] = menu