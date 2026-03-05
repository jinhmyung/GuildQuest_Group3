import json
import random
from profileManager import ProfileManager

class User():
    def __init__(self, fileName = "user.json"):
        self.fileName = fileName
        self.profile_manager = ProfileManager()

    def create_user(self, username: str, password: str) -> None:
        try:
            with open(self.fileName, "r") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}
    
        if username in data:
            print("User already exists!")
            return False
            
        profile_id = f"{username}_{random.randint(1000, 9999)}"
        self.profile_manager.create_profile(profile_id)

        data[username] = {
            "profile_id": profile_id,
            "password": password
        }
        with open(self.fileName, "w") as f:
            json.dump(data, f)
        
    def login(self, username: str, password: str) -> int:
        with open(self.fileName, "r") as f:
            data = json.load(f)
            if username in data and data[username]["password"] == password:
                print(username)
                profile_id = data[username]["profile_id"]
                print(profile_id)
                return self.profile_manager.load(profile_id)
        return False
    
    def login_cli(self):
        while True:
            print("\n==============================")
            print("GuildQuest CLI")
            print("==============================")
            username = input("Username: ").strip()
            password = input("Password: ").strip()
            
            login_result = self.login(username, password)

            if not login_result:
                print("Invalid username or password.")
                return False
            else:
                print("Login successful!")
                return login_result
    
    def create_cli(self):
        while True:
            print("\n==============================")
            print("GuildQuest CLI")
            print("==============================")
            username = input("Choose a username: ").strip()
            password = input("Choose a password: ").strip()
            
            
            create_result = self.create_user(username, password)
            if create_result:
                print("User created successfully!")
            else:
                print("User creation failed. Try again.")
            return 