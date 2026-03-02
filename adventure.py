from typing import List
from typing import Type
from typing import Optional
from miniAdventure import MiniAdventure

class AdventureFactory():
    def __init__(self):
        self.registry = {}
        self.adventureName = ""
        self.adventureID = 0

    def register(self, name: str, cls: Type[MiniAdventure]):
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
        return
    
    def get_selections(self):
        return
