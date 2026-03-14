import json
from playerProfile import PlayerProfile
import os

class ProfileManager:
    _instance = None  # holds the single instance

    def __new__(cls, filename="profiles.json"):
        if cls._instance is None:
            cls._instance = super(ProfileManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, filename="profiles.json"):
        if self._initialized:
            return

        self.filename = os.path.join(os.getcwd(), filename)
        self._initialized = True

    # Load data from profile_id into PlayerProfile object and return it
    def load(self, profile_id: str):
        with open(self.filename, "r") as f:
            data = json.load(f)
            if profile_id in data:
                profile = PlayerProfile(profile_id)
                profile.from_dict(data[profile_id])
                return profile

    # Save PlayerProfile data to file
    def save(self, profile_id: str, profile: PlayerProfile):
        try:
            with open(self.filename, "r") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}

        data[profile_id] = profile.to_dict()

        with open(self.filename, "w") as f:
            json.dump(data, f, indent=2)

    # Create new profile and save to file
    def create_profile(self, profile_id: str):
        try:
            with open(self.filename, "r") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}

        if profile_id in data:
            print("Profile already exists!")
            return

        profile = PlayerProfile(profile_id)
        profile.create_player_cli()

        self.save(profile_id, profile)

pm = ProfileManager()