# GuildQuest_Group3

In order to start running: 
    Python main.py
Change Realm’s to change miniGame difficulty/Monster:
	All inputs are inside the green box in the google drive version we have images !!!
---------------EXAMPLE-------------------

        ==============================
        GuildQuest CLI
        ==============================
        Current Realm: Grassfield (x: 0, y: 0)
        Player 1: (none)
        Player 2: (none)
        0) EXIT
        1) Create user
        2) Login user 1
        3) Login user 2
        4) MiniAdventure Menu
        5) Move Realm
        6) View P1 inventory
        7) View P2 inventory
        Choose: 5               #USER INPUT 5 IN ORDER TO VIEW REALMS

        ==============================
        Realms:

        1: Grassfield | Description: calm grassy lands | Coord:0,0
        2: Rockfield Deserts | Description: barren land | Coord:1,0
        3: IcePeak Summit | Description: treacherous mountains | Coord:2,0
        4: Galactic Zone | Description: outer space | Coord:3,0
        ==============================

        Enter Realm Coordinates: "x y" (0 to go back)
        0 0                      # PLAYER INPUT 0 0 TO ENTER INTO REALM CALLED Grassfield ENTER THE RIGHT MOST "Coord" numbers without the comma 
        Entered Realm Successfully
------------END EXAMPLE----------------

View Player Inventory: 
	Step 1: login player 1 or player 2 depending on which players inventory you wish to view 
	Ex. player 2’s inventory 


---------------EXAMPLE-------------------

        ==============================      
        GuildQuest CLI
        ==============================      
        Current Realm: Grassfield (x: 0, y: 0)
        Player 1: John
        Player 2: Crime
        0) EXIT
        1) Create user
        2) Login user 1
        3) Login user 2
        4) MiniAdventure Menu
        5) Move Realm
        6) View P1 inventory
        7) View P2 inventory
        Choose: 7

        ----- P2 Inventory -----
        Player: Crime
        1. Teeth  []  (uncommon)
        ==============================      
        Press Enter to continue...

------------END EXAMPLE----------------



Player a mini Game:
    STEP 1. login user 1 
    STEP 2. login user 2
    STEP 3. MiniAdventure Menu 
    example input: 
        Choose: 2
        Choose a username: ydureix
        choose a password: something123
        Choose: 3
        Choose a username: Criminal
        choose a password: crimes123
        Choose: 4
        what would you like to do? (enter 0 to end) : 1
	# Inside Mobhunt MiniGame
# select options to attack until monster is killed or player is killed and get













View Player Inventory: 
	Step 1: login player 1 or player 2 depending on which players inventory you wish to view 
	Ex. player 2’s inventory 
	
Player a mini Game:
    1. login user 1 
    2. login user 2
    3. MiniAdventure Menu 
    example input: 
        Choose: 2
        Choose a username: ydureix
        choose a password: something123
        Choose: 3
        Choose a username: Criminal
        choose a password: crimes123
        Choose: 4
        what would you like to do? (enter 0 to end) : 1
	# Inside Mobhunt MiniGame
# select options to attack until monster is killed or player is killed and get

---------------EXAMPLE-------------------

        ==============================
        GuildQuest CLI
        ==============================
        Current Realm: IcePeak Summit (x: 2, y: 0)
        Player 1: John  # PLAYER 1 LOGIN
        Player 2: Crime # PLAYER 2 LOGIN
        0) EXIT
        1) Create user
        2) Login user 1
        3) Login user 2
        4) MiniAdventure Menu
        5) Move Realm
        6) View P1 inventory
        7) View P2 inventory
		Choose: 4           # INPUT 4
        what would you like to do? (enter 0 to end) :
        1 : Mob Hunt
        2 : Treasure Trap
		1            # SELECT MINIGAME
        selected result Mob Hunt

        ==============================
        Mob Hunt Adventure
        ==============================
        Player 1: (John Rogue) HP: 100
        Player 2: (Crime Warrior) HP: 120
        Monster : (Dragon) HP: 300

        ==============================

        John's turn
        1. Attack
        2. Heavy Attack
        3. Special Attack
		Enter your choice (1-3): 1
        John attacks for 10 damage!

        ==============================
        Mob Hunt Adventure
        ==============================
        Player 1: (John Rogue) HP: 100
        Player 2: (Crime Warrior) HP: 120
        Monster : (Dragon) HP: 290

        ==============================


------------END EXAMPLE----------------

    It’s turn based so it will be player 1 then player2 then the monster until a player or the monster is dead. It is not possible to exit out of a game; it must be played till the end. 

Exiting the Game: 
    It’s possible to exit the game by entering 0 in GuildQuest CLI menu
