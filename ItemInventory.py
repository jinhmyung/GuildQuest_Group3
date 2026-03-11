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
    def __init__(self, tms:list):
        self.itemsList = tms   
    
    def AddItem(self, item_obj):
        self.itemsList.append(item_obj)
    
    def RemoveItem(self, index):
        del self.itemsList[index]

    def getItem(self, index):
        return self.itemsList[index]

    def getSize():
        return len(self.itemsList)
    
    def getAllItems(self):
        # this can be printed it's just a lsit
        return self.itemsList

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




class InventoryMenu:
    """"
        we will print out the list options and index self.action with the user selection to call the correct method 
        for the inventory menu. we also pass in the inventory items as the execute options so that when the user selects
         view inventory info we can print out all the items in the inventory
    """
    def __init__(self, storage):
        self.app = storage
        self.options = ["end app", "exit menu", "view inventory info", "add new item", "remove an item", "update item name"]
        self.executeOptions = storage.getAllItems()
        self.actions = { 
            0: exit, 
            1: None, # "exit menu" option it just returns back to the previous option
            2: self.InventoryInfo,
            3: self.addItem, 
            4: self.removeItem, 
            5: self.updateItemName}

    def MainMenu(self):
        # self.PrintOptions just loops through the print options and returns an input
        UserSelection = self.PrintOptions(self.options)
        while UserSelection != 1:
            self.actions.get(UserSelection)()
            UserSelection = self.PrintOptions(self.options)
    
        print("exiting Inventory Menu")
    
    def PrintOptions(self, list_obj):
        print(f"what would you like to do? (enter 0 to end) :") 
        for num, obj in enumerate(list_obj):
            print(f"{num} : {obj}")
        
        result = input().strip()
        if result.isdigit() and int(result) < len(list_obj):
            print(f"selected result {list_obj[int(result)]}")
            return int(result)
    
    def InventoryInfo(self):

        items = self.app.getAllItems()
        print("________________________________________")

        if len(items) == 0:
            print("no items to show")

        else:
            for item in items:
                print(item)
        print("________________________________________")


    def addItem(self):
        name = input("enter item name: ")
        rarity = Rarity_enum[self.PrintOptions(Rarity_enum)]
        tp = ItemType_enum[self.PrintOptions(ItemType_enum)]
        desc = input("enter item description: ")
        newItem = Item(name, rarity, tp, desc)
        self.app.AddItem(newItem)
    
    def removeItem(self):
        index = self.selectItem()
        self.app.RemoveItem(index)
    
    def updateItemName(self):
        index = self.selectItem()
        item = self.app.getItem(index)
        item.rename(input("enter new name for item: "))
    
    def selectItem(self):
        index = 0
        print("select Item to change")
        index = self.PrintOptions(self.app.getAllItems())
        if index > len(self.app.getAllItems()) - 1:
            print("invalid selection default realm has been selected`")
            return 0
        return index
    

    

Inventory1 = Inventory([])
menu = InventoryMenu(Inventory1)
menu.MainMenu()