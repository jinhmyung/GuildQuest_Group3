class PlayerProfile():
    def __init__(self):
        self.profile_id = ""
        self.character_name = ""
        self.preferred_realm = ""
        self.achievements = []
        self.quest_history = []
        self.inventory = []
    
    def to_dict(self):
        return
    
    def from_dict(self, data: dict):
        return