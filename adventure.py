from typing import List
from typing import Type
from typing import Optional
from miniAdventure import MiniAdventure

class AdventureFactory():
    def __init__(self):
        self.registry = {} #why does a factory class have a registry for adding multiple adventures but the factory has a single adventureName and ID for a single adventure?
        self.adventureName = ""
        self.adventureID = 0
    
    def getName(self):
        return self.adventureName

    def register(self, name: str, cls: Type[MiniAdventure]): #we are registering an adventure in a registry?
        self.registry[name] = cls

    def create(self, name: str) -> Optional[MiniAdventure]:
        if name in self.registry:
            return self.registry[name]()
        return None
    
    def list_adventures(self) -> List[str]:
        return list(self.registry.keys())
    

class AdventureMenu():
    def __init__(self):
        self.factory = AdventureFactory()

    def show_options(self):
        for adventure in self.factory.list_adventures:
            print(adventure.adventureName)
    
    def get_selections(self):
        return
