from abc import ABC, abstractmethod
from datetime import datetime, timedelta


class UIHangler:
    def __init__(self, wc, setting):
        self.wc = wc
        self.Setting = setting

    def PrintOptions(self, list_obj):
        print(f"what would you like to do? (enter 0 to end) :") 
        for num, obj in enumerate(list_obj):
            print(f"{num} : {obj}")
        
        result = input().strip()
        if result.isdigit() and int(result) < len(list_obj):
            print(f"selected result {list_obj[int(result)]}")
            return int(result)
        


    def printNonePresnt(self):
        print("not possible at the moment")


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


class MenuHelper(UIHangler, ABC):

    def __init__(self, app, options=[], exeOptions=[]):
        self.app = app
        self.options = options
        self.executeOptions = exeOptions

    @abstractmethod
    def MainMenu(self):
        pass


class MenuFactory(ABC):

    @abstractmethod
    def makeWorldEntity(self, *args):
        pass
    
    def create(self, *args):
        return self.makeWorldEntity(*args)


class RealmMenu(MenuHelper):
    def __init__(self, app):
        super().__init__(app, ["end app", "exit Realm", "view realm info", "add Realm", "remove Realm"], None)
        self.actions = {
            0: exit,
            1: None,
            2: self.viewRealmInfo,
            3: self.addRealm,
            4: self.removeRealm
        }    

    def MainMenu(self):
        UserSelection = self.PrintOptions(self.options)
        while UserSelection != 1:
            self.actions.get(UserSelection)()
            UserSelection = self.PrintOptions(self.options)
        print(f"{'-'*40}  exiting Realm  {'-'*40}")   

        
    def viewRealmInfo(self):
        print(f"{'-'*40}  Realms Info  {'-'*40}")
        if len(self.app) == 0:
            print("no realms to show")
        else:
            for realm in self.app:
                print(realm)
        print("-"*80)
    
    def addRealm(self):
        name = input("enter realm name: ")
        desc = input("enter realm description: ")
        wc = WorldClock()
        localT = int(input("enter realm time offset by hours: "))
        newRealm = Realm(name, desc, wc, localT)
        self.app.append(newRealm)
    
    def removeRealm(self):
        index = self.PrintOptions([name.getName() for name in self.app])
        if self.app[index].IsCurrentRealm():
            print("cant remove realm you are currently in")

        else: 
            del self.app[index]
        

class Realm(Entities):
    def __init__(self, name, description, WrldC, LocalTR, adjR=None):
        super().__init__(name, description, None)
        self.wc = WrldC            # string the description of the realm
        self.localTime = LocalTR     # int Time offset from world clock
        self.adjRealm = adjR        # Realm object that is adjacent to this realm
        self.isVisited = False
    
    def GetTime(self):
        return self.localTime

    def IsCurrentRealm(self):
        return self.isVisited
    
    def setVisited(self, val):
        self.isVisited = val

    def getName(self):
        return self.name

    def __str__(self):
        info = f""" 
            Realm Name:     {self.name}
            description:    {self.description}
            local time:    {self.localTime} hours from world clock
                """
        return info

class MenuWorldClock(MenuHelper):
    def __init__(self, WorldClokObj):
        super().__init__(WorldClokObj, ["Exit Menu", "world clock", "realm clock", "both"], None)

    def MainMenu(self):
        UserChoice = self.PrintOptions(self.options)
        if UserChoice == 0:     # exit menu
            return
        else:
            UserChoice -= 1
            self.app.updateTimeOption(UserChoice)
            print(self.app.getCurrentTime())

    def getTimeOption(self):
        return self.app.getTimeOption()


class TimeStrategy(ABC):
    @abstractmethod
    def getTime(self):
        pass
    
    @abstractmethod
    def printTime(self):
        pass


class RealmTime(TimeStrategy):
    def __init__(self, wc):
        self.wc = wc
        self.offset = 0

    def getTime(self):
        now = datetime.now() + timedelta(hours=self.offset)
        return now
    
    def printTime(self):
        time = "Realm Time is " + self.getTime().strftime("%A %B %d, %Y %I:%M %p")
        print(time)
    
    def setOffset(self, offset):
        self.offset = offset

class WorldTime(TimeStrategy):
    def __init__(self, wc):
        self.wc = wc

    def getTime(self):
        now = datetime.now()
        return now
    
    def printTime(self):
        time = "World Time is " + self.getTime().strftime("%A %B %d, %Y %I:%M %p")
        print(time)

    def setOffset(self, offset):
        pass

class BothTime(TimeStrategy):
    def __init__(self, wc):
        self.wc = wc
        self.offset = 0

    def getTime(self):
        worldTime = datetime.now().strftime("%A %B %d, %Y %I:%M %p")
        realmTime = (datetime.now() + timedelta(hours=self.offset)).strftime("%A %B %d, %Y %I:%M %p")
    
        return [worldTime, realmTime]

    def printTime(self):
        time = self.getTime()
        print(f"current world time is {time[0]}")
        print(f"current realm time is {time[1]}")

    def setOffset(self, offset):
        self.offset = offset

class WorldClock:
    instance = None
    
    def __new__(cls):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self, timeOption=WorldTime(instance)):
        if not hasattr(self, "_initalized"):
            self.TimeCls = timeOption 
            self._initialized = True
            self.RealmOffset = 0

    def updateTimeOption(self, UserOption):
        self.TimeCls = UserOption
        self.TimeCls.setOffset(self.RealmOffset)
    
    def getTimeOption(self):
        return self.TimeCls
    
    def makeTime(self, month, day, year, hr, mins):
        return datetime(year, month, day, hr, mins)

class Campaign(Entities):
    def __init__(self, name, Qst=[], vis="public"):
        super().__init__(name, None, Qst)
        self.visibility = vis  # default visibility
    
    def updateVisibility(self, vis):
        self.visibility = vis
    
    def getAllQuests(self):
        return self.List
    
    def getInfo(self):
        info = f""" 
        Campaign Name:  {self.name}
        Visibility:     {self.visibility}
        Quests:         {[q.getName() for q in self.List]}
        """
        return info
    
    def __str__(self):
        return "campaign"

class CampaignMenu(MenuHelper):
    def __init__(self, app):
        super().__init__(app, ["end app", "exit menu", "view campaign info", "add new campaign", "remove a campaign", "update name", "update visibility", "add a quest to campaign", "remove a quest from campaign"], None)
        self.CampObjs = app.AllCamp
        self.viz_op = ["public", "private"]

        self.actions = {
            0: exit,
            1: None,
            2: self.viewCampaignInfo,
            3: self.addCampaign,
            4: self.removeCampaign,
            5: self.updateCampaignName,
            6: self.changeCampaignVisibility,
            7: self.addQuestToCamp,
            8: self.removeQuestFromCamp
        }

    def MainMenu(self):
        UserSelection = self.PrintOptions(self.options)
        while UserSelection != 1:
            self.actions.get(UserSelection)()
            UserSelection = self.PrintOptions(self.options)
        print("exiting Campaign Menu")
            
    
    def viewCampaignInfo(self):
        print(f"{'-'*40}  Campaigns Info  {'-'*40}")
        if len(self.CampObjs) == 0:
            print("no campaigns to show")
        else:
            for c in self.CampObjs:
                print(c.getInfo())
        print("-"*80)
    
    def addCampaign(self):
        name = input("enter Campaign name: ")
        QuestsInCamp = []
        if input("press y to enter an existing quest for this new Campaign").strip().upper() == "Y":
            inx = self.PrintOptions([qst for qst in self.app.AllQst])
            QuestsInCamp.append(self.app.AllQst[inx])
        
        visibility = self.PrintOptions(self.viz_op)
        self.CampObjs.append(Campaign(name, QuestsInCamp, self.viz_op[visibility]))

    def removeCampaign(self):
        index = self.selectCampaign()
        del self.CampObjs[index]
    
    def updateCampaignName(self):
        index = self.selectCampaign()
        self.Camp = self.CampObjs[index]
        self.Camp.rename(input("enter new name for campaign: "))
    
    def addQuestToCamp(self):
        index = self.selectCampaign()
        Camp = self.CampObjs[index]
        print("-"*40 + "select quest to add to campaign" + "-"*40)
        questToAdd = self.PrintOptions([qst for qst in self.app.AllQst])
        Camp.addEntity(self.app.AllQst[questToAdd])
    
    def removeQuestFromCamp(self):
        index = self.selectCampaign()
        print("-"*40 + "select quest to remove from campaign" + "-"*40)

        Camp = self.CampObjs[index]
    
        questToRemove = self.PrintOptions([qst for qst in Camp.getAllQuests()])
        Camp.removeEntity(questToRemove)
    
    def updateCampaignVisibility(self):
        index = self.selectCampaign()
        self.Camp = self.CampObjs[index]
        visibility = self.PrintOptions(self.viz_op)
        self.Camp.updateVisibility(self.viz_op[visibility])
    
    def updateCampaignName(self):
        index = self.selectCampaign()
        self.Camp = self.CampObjs[index]
        self.Camp.rename(input("enter new name for campaign: "))
    
    def addQuestToCamp(self):
        index = self.selectCampaign()
        Camp = self.CampObjs[index]
        print("-"*40 + "select quest to add to campaign" + "-"*40)
        questToAdd = self.PrintOptions([qst for qst in self.app.AllQst])
        Camp.addEntity(self.app.AllQst[questToAdd])

    def selectCampaign(self):
        index = 0
        print("-"*40 + "select Campaign to change" + "-"*40)
        index = self.PrintOptions([C.getInfo() for C in self.CampObjs])
        if index > len(self.CampObjs) - 1:
            print("invalid selection default realm has been selected`")
            return 0
        return index
    
    def changeCampaignVisibility(self):
        index = self.PrintOptions([C.getInfo() for C in self.CampObjs])
    
        visibility = self.PrintOptions(self.viz_op)
        self.CampObjs[index].updateVisibility(self.viz_op[visibility])
    

class QuestEvent(Entities):

    def __init__(self, name, description, startT, endT, locat, players=[], rewards=[]):
        super().__init__(name, description, rewards)
        self.startTine = startT # Time obj
        self.endTime = endT     # Time obj
        self.location = locat   # realm_obj
        self.party = players    # [Name of character objects]
    

    def updateStartTime(self, Tme):
        self.startTine = Tme
    
    def updateEndTime(self, Tme):
        self.endTime = Tme
    
    def updateLocation(self, Rlm):
        self.location = Rlm
    
    def createTime(self, month, day, year, hr, mins):
        wc = WorldClock()
        return wc.makeTime(month, day, year, hr, mins)
    
    def addParticipants(self, Char):
        self.party.append(Char)
    
    def __str__(self):
        info = f""" 
                Quest Name:     {self.name}
                Description:    {self.description}
                Start Time:     {self.startTine}
                End Time:       {self.endTime}
                Location:       {self.location.getName()}
                Rewards:        {[item for item in self.List]}
                Participants    {self.party}
        """
        return info

class QuestMenu(MenuHelper):
    def __init__(self, app):
        super().__init__(app, ["end app", "exit menu", "view quest info", "add new quest", "remove existing quest", "update name", "update start time", "update end time", "update location"], app.AllQst)
        self.AllRealms = app.AllRealm

    def MainMenu(self):
        while True:
            UserSelection = self.PrintOptions(self.options)
            
            if UserSelection == 0:
                exit()
            
            elif UserSelection == 1:
                return
            
            elif UserSelection == 2:
                for q in self.executeOptions:
                    print(q)
  
            elif UserSelection == 3:
                #self, nm, startT, endT, locat, players=[], rwds=[]
                name = input("enter quest name: ")
                description = input("enter quest description: ")
                startTime = self.changeQuestTime("start")
                
                if input("press y to enter end time ").strip().upper() == "Y":
                    newEndTime = self.changeQuestTime("end")
                else:
                    newEndTime = None
                
                if input("press y to enter participants ").strip().upper() == "Y":
                    participants = input("enter quest participants separate by comma: ").split(",")
                else:
                    participants = []
        
                location = self.selectRealmForQuest()
                print((f"selected location is {type(location)}"))


                self.executeOptions.append(QuestEvent(name, description, startTime, newEndTime, location, participants, []))

            elif UserSelection == 4:
                index = self.selectQuest()
                del self.executeOptions[index]

            elif UserSelection == 5:
                index = self.selectQuest()
                self.QstEvnt = self.executeOptions[index]
                self.QstEvnt.rename(input("enter new name for quest: "))
            
            elif UserSelection == 6:
                index = self.PrintOptions(self.executeOptions)
                self.QstEvnt = self.executeOptions[index]

                newStartTime = self.changeQuestTime("start")
                self.QstEvnt.updateStartTime(newStartTime)
            
            elif UserSelection == 7:
                index = self.PrintOptions(self.executeOptions)
                self.QstEvnt = self.executeOptions[index]

                newEndTime = self.changeQuestTime("end")
                self.QstEvnt.updateEndTime(newEndTime)
            
            elif UserSelection == 8:
                index = self.PrintOptions(self.executeOptions)
                self.QstEvnt = self.executeOptions[index]
                newLocation = self.selectRealmForQuest()
                self.QstEvnt.updateLocation(newLocation)
        
    def selectQuest(self):
        index = 0
        print("select quest to change")
        index = self.PrintOptions(self.executeOptions)
        if index > len(self.executeOptions) - 1:
            print("invalid selection default realm has been selected`")
            return 0
        return index

    def selectRealmForQuest(self):
        print("select realm for quest")
        index = self.PrintOptions(self.AllRealms)

        return self.AllRealms[index]
    
    def changeQuestName(self):
        newName = input("enter new name for quest: ")
        self.QstEvnt.updateName(newName)
    
    def changeQuestTime(self, newTime):
        print(f"enter {newTime} time for quest as M/d/Y hr:mim")
        month = input("enter month: ").strip()
        day = input("enter day: ").strip()
        year = input("enter year: ").strip()
        hour = input("enter time ex. 12: ").strip()
        mins = input("enter mins ex. 30: ").strip()


        newStartTime = WorldClock().makeTime(int(month), int(day), int(year), int(hour), int(mins))
        return newStartTime

class User(UIHangler):
    def __init__(self, nme, camps=[], onlyQuests=[], chars=[]):
        self.name = nme         
        self.campaigns = camps        # {int campaign_obj}
        self.orphanQuests = onlyQuests  # {int, Quest_obj} Quests without campaigns
        self.characters = chars         # {int, Character_obj}
        self.activeChar = chars[0] if chars else None

    def setActiveCharacter(self, char):
        self.activeChar = char

    def getCurrentCharacter(self):
        return self.activeChar

    def addCampaign(self, Camp):
        self.campaigns[Camp.getID()] = Camp    


class Character(Entities):

    def __init__(self, name, characterClass, lvl=1, storage=None):
        super().__init__(name, characterClass, storage)
        self.level = lvl                # int
    
    def getLevel(self):
        return self.level
    
    def updateLevel(self, offset):
        self.level += offset
    
    def __str__(self):
        info = f""" 
                Character Name: {self.name}
                Class:          {self.description} 
                Level:          {self.level}
                """
        return info
    
    def getInventory(self):
        return self.getEntity()
    
class Inventory:
    def __init__(self, tms):
        self.itemsDict = tms    # Dict of items
    
    def AddItem(self, item_obj):
        self.itemsDict.append(item_obj)
    
    def RemoveItem(self, index):
        del self.itemsDict[index]

    def getItem(self, index):
        return self.itemsDict[index]

    def getSize():
        return len(self.itemsDict)
    
    def getAllItems(self):
        return self.itemsDict


Rarity_enum = ["common", "uncommon", "rare", "epic", "legendary"]
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




class InventoryMenu(MenuHelper):

    def __init__(self, storage):
        """"
        we will print out the list options and index self.action with the user selection to call the correct method 
        for the inventory menu. we also pass in the inventory items as the execute options so that when the user selects
         view inventory info we can print out all the items in the inventory
        """
        super().__init__(storage, ["end app", "exit menu", "view inventory info", "add new item", "remove an item", "update item name"], storage.getAllItems())
        self.actions = { 
            0: exit, 
            1: None,
            2: self.InventoryInfo,
            3: self.addItem, 
            4: self.removeItem, 
            5: self.updateItemName}

    def MainMenu(self):
        UserSelection = self.PrintOptions(self.options)
        while UserSelection != 1:
            self.actions.get(UserSelection)()
            UserSelection = self.PrintOptions(self.options)
    
        print("exiting Inventory Menu")
            
    
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
    
    def changeCampaignVisibility(self):
        index = self.PrintOptions([C.getInfo() for C in self.CampObjs])
    
        viz_op = ["public", "private"]
        visibility = self.PrintOptions(viz_op)
        self.CampObjs[index].updateVisibility(viz_op[visibility])

class SettingsMenu(MenuHelper):
    def __init__(self, app, wc):
        """
        I have a super that just store the the class for settings as app 
        the list is the user options which gets sent to a for loop that print
        them with numbers to the left then when a number is selected it is used to 
        index self.actions and call the method connected the that number.
        """
        super().__init__(app, ["end app", "exit menu", "change to next realm", "change time option"], None)
        self.wc = wc


        self.actions = {
            0: exit,
            1: None,
            2: self.nextRealm,
            3: self.changeTimeOption
        }

        # we create a time strategy object for each time option and store them in a dict
        # so that when the user selects a time option we can just call the getTime method
        #  on the correct time strategy object to get the correct time based on the current realm offset
        self.selectedTime = {
            0: WorldTime(wc),
            1: RealmTime(wc),
            2: BothTime(wc)
        }


    def MainMenu(self):
        UserChoice = self.PrintOptions(self.options)
        while UserChoice != 1:
            self.actions.get(UserChoice)()
            UserChoice = self.PrintOptions(self.options)
        print("exiting Settings Menu")
    
    def nextRealm(self):
        self.app.nextRealm()
        self.wc.app.RealmOffset = self.app.getCurrentRealm().GetTime()
    
    def changeTimeOption(self):
        timeoptions = ["world clock", "realm clock", "both"]

        self.wc.app.updateTimeOption(self.selectedTime[self.PrintOptions(timeoptions)])
        self.wc.app.getTimeOption().printTime()

class Settings:
    def __init__(self, app, wc):
        self.AllRealms = app
        self.current = 0
        self.themeIsModern = True
        self.timeOption = 0 # 0 world clock, 1 realm clock, 2 both
        self.wc = wc #world clock object to get time from

    def nextRealm(self):
        """
        there switches to the next realm in the list but doesn't go out of bounds because of the
         modulus operator. it also sets the current realm to not visited and the new realm to 
         visited so that the app can keep track of
         which realm the user is currently in
        """
        print("*"*80)
        self.AllRealms[self.current].setVisited(False)
        self.current = (self.current + 1) % len(self.AllRealms)
        self.AllRealms[self.current].setVisited(True)
        print(self.getCurrentRealm())
        print("*"*80)
    
    def getCurrentRealm(self):
        return self.AllRealms[self.current]

    
    def getTimeOption(self):
        return self.timeOption

class GuildQuestMenuFactory(MenuFactory):

    def makeWorldEntity(self, indx):
        result = {
        1: [SettingsMenu, (app.Setting, MenuWorldClock(app.WorldClock))],
        3: [RealmMenu, (app.AllRealm,)],
        4: [CampaignMenu, (app,)],
        5: [QuestMenu, (app,)],
        6: [InventoryMenu, (app.getCharacter().getInventory(),)] #pass in inventory items and all quests for quest rewards
        }

    
        choice = result.get(indx)
        NewClass = choice[0]
        args = choice[1]
        
        # makes a new menu object based on user selection and passes in the correct arguments for that menu
        return NewClass(*args)

    

class GuildQuestMenu(MenuHelper):

    def __init__(self, APP):
        super().__init__(APP, ["end app", "settings", "User Menu", "Realm Menu", "Campaign Menu", "Quest Menu", "Inventory Menu"], None)
        self.MFactory = GuildQuestMenuFactory()
        

    def MainMenu(self):
        UserChoice = self.PrintOptions(self.options)
        while UserChoice != 0:
            if UserChoice == 2:     # User Menu
                print("not possible at the moment")
            else:
                menu = self.MFactory.create(UserChoice).MainMenu()

            UserChoice = self.PrintOptions(self.options)


class GuildQuestApp(UIHangler):
    def __init__(self, UsObj, WC, sett, Rlm, AlUsers, AlCamp, AlQust, AlRelm):
        self.User = UsObj
        self.WorldClock = WC
        self.Setting = sett          # settings object
        self.Realm = Rlm            # current realm obj
        self.AllUsers = AlUsers     # dict{String, User}
        self.AllCamp = AlCamp       # dict{int, camp}
        self.AllQst = AlQust        # dict{int, Quest}
        self.AllRealm = AlRelm      # dict{int, Ream}
        self.timeOption = 0 # 0 world clock, 1 realm clock, 2 both

    def setCharacter(self, char):
        self.User.setActiveCharacter(char)
    
    def getCharacter(self):
        return self.User.getCurrentCharacter()
    
    def getCurrentRealm(self):
        return self.Setting.getCurrentRealm()
    
    def getRealmTime(self):
        return self.Setting.getCurrentRealm().GetTime()

def default_elems():
    wc = WorldClock()
    Item1 = Item("item1", Rarity_enum[0], ItemType_enum[3], "the first item")
    Item2 = Item("item2", Rarity_enum[1], ItemType_enum[2], "the second item")
    Inventory1 = Inventory([Item1, Item2])


    realm1 = Realm("realm1", "the first realm", wc, 0)
    realm2 = Realm("realm2", "the second realm", wc, 5)
    realm3 = Realm("realm3", "the third realm", wc, -3)
    AllRealm = [realm1, realm2, realm3]
    sett = Settings(AllRealm, wc)
    quest1 = QuestEvent("quest1", "the first quest", wc.makeTime(1, 1, 2026, 12, 0), wc.makeTime(1, 2, 2026, 12, 0), realm1, ["Ducky"], [Item1])
    quest2 = QuestEvent("quest2", "the second quest", wc.makeTime(1, 3, 2026, 12, 0), wc.makeTime(1, 4, 2026, 12, 0), realm2, ["MoMo"], [Item2])
    Character1 = Character("default character", "a default character", 2, Inventory1)

    AlQust = [quest1, quest2]
    AlRelm = [realm1, realm2, realm3]
    Campaign1 = Campaign("default campaign", AlQust, "public")

    User1 = User("default user", [], [], [Character1])

    return GuildQuestApp(User1, wc, sett, realm1, [User1], [Campaign1], AlQust, AlRelm)

if __name__ == "__main__":
    print("Hello welcome to GuildQuest")
    print("Loading default world and player...")

    app = default_elems()
    app.setCharacter(app.User.characters[0])
    things = GuildQuestMenu(app)
    things.MainMenu()



    
    




    




    

        