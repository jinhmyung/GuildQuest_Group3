from abc import ABC, abstractmethod

# this class is used by items later for some basic stuff 
class Entities(ABC):
    def __init__(self, name, description, EntList=[]):
        self.name = name
        self.description = description
        self.List = EntList
    
    def getName(self):
        return self.name

    def rename(self, name):
        self.name = name

    def removeEntity(self, index):
        if index < len(self.List):
            del self.List[index]

    def addEntity(self, NewObject):
        self.List.append(NewObject)

    def getEntity(self):
        return self.List

    def updateEntity(self, index):
        if index < len(self.List):
            return self.List[index]

    @abstractmethod
    def __str__(self):
        pass

class Inventory:
    def __init__(self, tms=None):
        if tms is None:
            self.itemsList = []
        else:
            self.itemsList = tms
    
    def AddItem(self, item_obj):
        self.itemsList.append(item_obj)
    
    def RemoveItem(self, index):
        del self.itemsList[index]

    def getItem(self, index):
        return self.itemsList[index]

    def getSize(self):
        return len(self.itemsList)
    
    def getAllItems(self):
        # this can be printed it's just a lsit
        return self.itemsList
    
    def to_dict(self):
        # this might matter if we need to save the users attack power or hp if it goes up
        jsonList = []
        if len(self.itemsList) > 0:
            for item in self.itemsList:
                jsonList.append(item.to_dict())
        return jsonList
    
    def from_dict(self, data):
        self.itemsList = []  # clear inventory first
        for item in data:
            self.itemsList.append(
                Item(item["name"], item["rarity"], item["type"], item["description"])
            )


# rarity can be removed or changed it's never really used just printed lines 27, 33, 84,
Rarity_enum = ["common", "uncommon", "rare", "epic", "legendary"]
# this one just gives options of item type it can be changed/removed
ItemType_enum = ["weapon", "armor", "Tool", "Trinket", "Food"]

class Item(Entities):
    def __init__(self, name, rare=Rarity_enum[0], tp=ItemType_enum[2], description=""):
        super().__init__(name, description, [])
        self.rarity = rare
        self.type = tp
    
    def __str__(self):
        info = f""" 
                Item Name:      {self.name}
                Rarity:         {self.rarity} 
                type:           {self.type}
                description:    {self.description}
                """
        return info

    def to_dict(self):
        return {"name": self.name, "rarity": self.rarity,  "type": self.type, "description": self.description}

