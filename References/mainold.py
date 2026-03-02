from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Dict, List, Optional, Tuple


# =========================
# Enums
# =========================

class Visibility(str, Enum):
    PUBLIC = "PUBLIC"
    PRIVATE = "PRIVATE"


class PermissionLevel(str, Enum):
    VIEW_ONLY = "VIEW_ONLY"
    COLLABORATIVE = "COLLABORATIVE"


class TimeDisplayPreference(str, Enum):
    WORLD = "WORLD"
    LOCAL = "LOCAL"
    BOTH = "BOTH"


class TimeRangeType(str, Enum):
    DAY = "DAY"
    WEEK = "WEEK"
    MONTH = "MONTH"
    YEAR = "YEAR"


# =========================
# Time Model
# =========================

@dataclass(frozen=True)
class WorldClockTime:
    day: int
    hour: int
    minute: int

    def __post_init__(self) -> None:
        if self.day < 0:
            raise ValueError("day must be >= 0")
        if not (0 <= self.hour <= 23):
            raise ValueError("hour must be 0..23")
        if not (0 <= self.minute <= 59):
            raise ValueError("minute must be 0..59")

    def to_minutes(self) -> int:
        return self.day * 24 * 60 + self.hour * 60 + self.minute

    def plus_minutes(self, delta: int) -> "WorldClockTime":
        total = self.to_minutes() + delta
        if total < 0:
            raise ValueError("time cannot go negative")
        day = total // (24 * 60)
        rem = total % (24 * 60)
        hour = rem // 60
        minute = rem % 60
        return WorldClockTime(day=day, hour=hour, minute=minute)

    def __str__(self) -> str:
        return f"Day {self.day} {self.hour:02d}:{self.minute:02d}"


# =========================
# Realm / Settings
# =========================

@dataclass
class RealmTimeRule:
    offset_minutes: int = 0
    day_length_multiplier: float = 1.0  # optional future extension

    def to_local(self, world_time: WorldClockTime) -> WorldClockTime:
        # initial version: simple fixed offset
        return world_time.plus_minutes(self.offset_minutes)


@dataclass
class Realm:
    realm_id: str
    name: str
    description: str = ""
    map_id: int = 0
    x_coord: int = 0
    y_coord: int = 0
    time_rule: RealmTimeRule = field(default_factory=RealmTimeRule)


@dataclass
class Settings:
    current_realm_id: str
    theme: str = "classic"
    time_display: TimeDisplayPreference = TimeDisplayPreference.WORLD

    def set_time_display(self, pref: TimeDisplayPreference) -> None:
        self.time_display = pref


# =========================
# RPG Domain
# =========================

@dataclass
class InventoryItem:
    name: str
    description: str = ""
    type: str = "misc"
    rarity: int = 0


@dataclass
class Character:
    char_id: str
    name: str
    class_name: str
    level: int = 1
    inventory: List[InventoryItem] = field(default_factory=list)

    def add_item(self, item: InventoryItem) -> None:
        self.inventory.append(item)

    def remove_item_by_name(self, item_name: str, qty: int = 1) -> int:
        removed = 0
        for it in list(self.inventory):
            if removed >= qty:
                break
            if it.name == item_name:
                self.inventory.remove(it)
                removed += 1
        return removed


@dataclass
class InventoryChange:
    item: InventoryItem
    delta_qty: int
    target_char_id: Optional[str] = None


# =========================
# Sharing
# =========================

@dataclass
class Share:
    shared_with_user: str
    permission: PermissionLevel


# =========================
# QuestEvent / Campaign / User
# =========================

@dataclass
class QuestEvent:
    event_id: str
    name: str
    start_time: WorldClockTime
    end_time: Optional[WorldClockTime]
    realm_id: str
    participant_char_ids: List[str] = field(default_factory=list)
    shares: List[Share] = field(default_factory=list)  # event-level share
    inventory_changes: List[InventoryChange] = field(default_factory=list)

    def share_with(self, username: str, permission: PermissionLevel) -> None:
        for s in self.shares:
            if s.shared_with_user == username:
                s.permission = permission
                return
        self.shares.append(Share(shared_with_user=username, permission=permission))

    def unshare_with(self, username: str) -> None:
        self.shares = [s for s in self.shares if s.shared_with_user != username]

    def get_permission(self, username: str, owner_username: str) -> Optional[PermissionLevel]:
        if username == owner_username:
            return PermissionLevel.COLLABORATIVE
        for s in self.shares:
            if s.shared_with_user == username:
                return s.permission
        return None


@dataclass
class Campaign:
    campaign_id: str
    owner_username: str
    name: str
    visibility: Visibility = Visibility.PRIVATE
    archived: bool = False
    quest_event_ids: List[str] = field(default_factory=list)
    shares: List[Share] = field(default_factory=list)  # campaign-level share

    def share_with(self, username: str, permission: PermissionLevel) -> None:
        if username == self.owner_username:
            return
        for s in self.shares:
            if s.shared_with_user == username:
                s.permission = permission
                return
        self.shares.append(Share(shared_with_user=username, permission=permission))

    def unshare_with(self, username: str) -> None:
        self.shares = [s for s in self.shares if s.shared_with_user != username]

    def get_permission(self, username: str) -> Optional[PermissionLevel]:
        if username == self.owner_username:
            return PermissionLevel.COLLABORATIVE
        if self.visibility == Visibility.PUBLIC:
            return PermissionLevel.VIEW_ONLY
        for s in self.shares:
            if s.shared_with_user == username:
                return s.permission
        return None

    def can_view(self, username: str) -> bool:
        return self.get_permission(username) is not None

    def can_edit(self, username: str) -> bool:
        return self.get_permission(username) == PermissionLevel.COLLABORATIVE


@dataclass
class User:
    username: str
    settings: Settings
    campaign_ids: List[str] = field(default_factory=list)
    character_ids: List[str] = field(default_factory=list)


# =========================
# Storage / App
# =========================

def _safe_int(prompt: str, min_v: Optional[int] = None, max_v: Optional[int] = None) -> int:
    while True:
        s = input(prompt).strip()
        try:
            v = int(s)
            if min_v is not None and v < min_v:
                print(f"Must be >= {min_v}")
                continue
            if max_v is not None and v > max_v:
                print(f"Must be <= {max_v}")
                continue
            return v
        except ValueError:
            print("Please enter an integer.")


def _pick_from_list(title: str, items: List[Tuple[str, str]]) -> Optional[str]:
    """
    items: list of (id, display)
    returns selected id or None
    """
    if not items:
        print("(none)")
        return None
    print(title)
    for i, (_, disp) in enumerate(items, start=1):
        print(f"  {i}. {disp}")
    print("  0. Cancel")
    choice = _safe_int("Choose: ", 0, len(items))
    if choice == 0:
        return None
    return items[choice - 1][0]


def _parse_time(label: str) -> WorldClockTime:
    print(f"Enter {label} time:")
    day = _safe_int("  day (>=0): ", 0, None)
    hour = _safe_int("  hour (0-23): ", 0, 23)
    minute = _safe_int("  minute (0-59): ", 0, 59)
    return WorldClockTime(day, hour, minute)


class GuildQuestApp:
    def __init__(self) -> None:
        self.users: Dict[str, User] = {}
        self.realms: Dict[str, Realm] = {}
        self.campaigns: Dict[str, Campaign] = {}
        self.events: Dict[str, QuestEvent] = {}
        self.characters: Dict[str, Character] = {}
        self._id_counters: Dict[str, int] = {"realm": 1, "campaign": 1, "event": 1, "char": 1}
        self.current_user: Optional[str] = None

    # ---------- ID helpers ----------
    def _new_id(self, kind: str, prefix: str) -> str:
        n = self._id_counters.get(kind, 1)
        self._id_counters[kind] = n + 1
        return f"{prefix}{n}"

    # ---------- Persistence ----------
    def save(self, path: str = "guildquest_data.json") -> None:
        payload = {
            "id_counters": self._id_counters,
            "current_user": self.current_user,
            "users": {k: asdict(v) for k, v in self.users.items()},
            "realms": {k: self._realm_to_dict(v) for k, v in self.realms.items()},
            "campaigns": {k: self._campaign_to_dict(v) for k, v in self.campaigns.items()},
            "events": {k: self._event_to_dict(v) for k, v in self.events.items()},
            "characters": {k: self._character_to_dict(v) for k, v in self.characters.items()},
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
        print(f"Saved to {path}")

    def load(self, path: str = "guildquest_data.json") -> None:
        try:
            with open(path, "r", encoding="utf-8") as f:
                payload = json.load(f)
        except FileNotFoundError:
            print("No saved file found.")
            return

        self._id_counters = payload.get("id_counters", self._id_counters)
        self.current_user = payload.get("current_user", None)

        self.users = {}
        for username, ud in payload.get("users", {}).items():
            settings = Settings(
                current_realm_id=ud["settings"]["current_realm_id"],
                theme=ud["settings"].get("theme", "classic"),
                time_display=TimeDisplayPreference(ud["settings"].get("time_display", "WORLD")),
            )
            self.users[username] = User(
                username=username,
                settings=settings,
                campaign_ids=ud.get("campaign_ids", []),
                character_ids=ud.get("character_ids", []),
            )

        self.realms = {rid: self._dict_to_realm(d) for rid, d in payload.get("realms", {}).items()}
        self.campaigns = {cid: self._dict_to_campaign(d) for cid, d in payload.get("campaigns", {}).items()}
        self.events = {eid: self._dict_to_event(d) for eid, d in payload.get("events", {}).items()}
        self.characters = {chid: self._dict_to_character(d) for chid, d in payload.get("characters", {}).items()}

        print(f"Loaded from {path}")
        if self.current_user and self.current_user not in self.users:
            self.current_user = None

    # ---------- Serialization helpers ----------
    def _realm_to_dict(self, r: Realm) -> dict:
        d = asdict(r)
        # enums not present here
        return d

    def _dict_to_realm(self, d: dict) -> Realm:
        tr = d.get("time_rule", {})
        rule = RealmTimeRule(
            offset_minutes=tr.get("offset_minutes", 0),
            day_length_multiplier=tr.get("day_length_multiplier", 1.0),
        )
        return Realm(
            realm_id=d["realm_id"],
            name=d["name"],
            description=d.get("description", ""),
            map_id=d.get("map_id", 0),
            x_coord=d.get("x_coord", 0),
            y_coord=d.get("y_coord", 0),
            time_rule=rule,
        )

    def _campaign_to_dict(self, c: Campaign) -> dict:
        d = asdict(c)
        d["visibility"] = c.visibility.value
        # shares permission is enum -> value already due to asdict, but ensure:
        for s in d.get("shares", []):
            s["permission"] = str(s["permission"])
        return d

    def _dict_to_campaign(self, d: dict) -> Campaign:
        shares = [Share(shared_with_user=s["shared_with_user"], permission=PermissionLevel(s["permission"]))
                  for s in d.get("shares", [])]
        return Campaign(
            campaign_id=d["campaign_id"],
            owner_username=d["owner_username"],
            name=d["name"],
            visibility=Visibility(d.get("visibility", "PRIVATE")),
            archived=bool(d.get("archived", False)),
            quest_event_ids=d.get("quest_event_ids", []),
            shares=shares,
        )

    def _event_to_dict(self, e: QuestEvent) -> dict:
        d = asdict(e)
        d["start_time"] = asdict(e.start_time)
        d["end_time"] = asdict(e.end_time) if e.end_time else None
        for s in d.get("shares", []):
            s["permission"] = str(s["permission"])
        # inventory changes
        inv = []
        for chg in e.inventory_changes:
            inv.append({
                "item": asdict(chg.item),
                "delta_qty": chg.delta_qty,
                "target_char_id": chg.target_char_id
            })
        d["inventory_changes"] = inv
        return d

    def _dict_to_event(self, d: dict) -> QuestEvent:
        st = d["start_time"]
        et = d.get("end_time")
        start_time = WorldClockTime(st["day"], st["hour"], st["minute"])
        end_time = WorldClockTime(et["day"], et["hour"], et["minute"]) if et else None
        shares = [Share(shared_with_user=s["shared_with_user"], permission=PermissionLevel(s["permission"]))
                  for s in d.get("shares", [])]
        inv_changes = []
        for chg in d.get("inventory_changes", []):
            itemd = chg["item"]
            item = InventoryItem(**itemd)
            inv_changes.append(InventoryChange(item=item, delta_qty=int(chg["delta_qty"]),
                                               target_char_id=chg.get("target_char_id")))
        return QuestEvent(
            event_id=d["event_id"],
            name=d["name"],
            start_time=start_time,
            end_time=end_time,
            realm_id=d["realm_id"],
            participant_char_ids=d.get("participant_char_ids", []),
            shares=shares,
            inventory_changes=inv_changes,
        )

    def _character_to_dict(self, c: Character) -> dict:
        d = asdict(c)
        return d

    def _dict_to_character(self, d: dict) -> Character:
        inv = [InventoryItem(**it) for it in d.get("inventory", [])]
        return Character(
            char_id=d["char_id"],
            name=d["name"],
            class_name=d["class_name"],
            level=int(d.get("level", 1)),
            inventory=inv,
        )

    # =========================
    # Core operations
    # =========================

    def ensure_default_realm(self) -> None:
        if self.realms:
            return
        rid = self._new_id("realm", "R")
        self.realms[rid] = Realm(realm_id=rid, name="Earth", description="Default realm", map_id=1,
                                 time_rule=RealmTimeRule(offset_minutes=0))
        print("Created default realm: Earth (R1)")

    def create_user(self) -> None:
        username = input("New username: ").strip()
        if not username:
            print("Username cannot be empty.")
            return
        if username in self.users:
            print("User already exists.")
            return
        self.ensure_default_realm()
        default_realm_id = next(iter(self.realms.keys()))
        settings = Settings(current_realm_id=default_realm_id)
        self.users[username] = User(username=username, settings=settings)
        self.current_user = username
        print(f"Created and logged in as {username}")

    def login(self) -> None:
        if not self.users:
            print("No users yet. Create one.")
            return
        items = [(u, f"{u}") for u in self.users.keys()]
        chosen = _pick_from_list("Users:", items)
        if chosen:
            self.current_user = chosen
            print(f"Logged in as {chosen}")

    def require_login(self) -> Optional[User]:
        if not self.current_user or self.current_user not in self.users:
            print("Please login first.")
            return None
        return self.users[self.current_user]

    # ---------- Realms ----------
    def list_realms(self) -> None:
        if not self.realms:
            print("(no realms)")
            return
        for r in self.realms.values():
            off = r.time_rule.offset_minutes
            print(f"- {r.realm_id}: {r.name} (offset {off} min) desc='{r.description}'")

    def create_realm(self) -> None:
        rid = self._new_id("realm", "R")
        name = input("Realm name: ").strip()
        desc = input("Description (optional): ").strip()
        map_id = _safe_int("mapID (int, optional, default 0): ", 0, None)
        x = _safe_int("x_coord (int, optional, default 0): ", -10**9, 10**9)
        y = _safe_int("y_coord (int, optional, default 0): ", -10**9, 10**9)
        offset = _safe_int("time offset minutes (can be negative): ", -10**9, 10**9)
        self.realms[rid] = Realm(
            realm_id=rid, name=name or f"Realm{rid}", description=desc, map_id=map_id, x_coord=x, y_coord=y,
            time_rule=RealmTimeRule(offset_minutes=offset)
        )
        print(f"Created realm {rid}: {self.realms[rid].name}")

    # ---------- Settings ----------
    def edit_settings(self) -> None:
        user = self.require_login()
        if not user:
            return
        while True:
            cur_realm = self.realms.get(user.settings.current_realm_id)
            print("\n--- Settings ---")
            print(f"User: {user.username}")
            print(f"Current realm: {cur_realm.name if cur_realm else user.settings.current_realm_id}")
            print(f"Theme: {user.settings.theme}")
            print(f"Time display: {user.settings.time_display.value}")
            print("1) Change current realm")
            print("2) Change theme")
            print("3) Set time display (WORLD/LOCAL/BOTH)")
            print("0) Back")
            c = input("Choose: ").strip()
            if c == "1":
                rid = _pick_from_list("Pick realm:", [(r.realm_id, f"{r.realm_id} {r.name}") for r in self.realms.values()])
                if rid:
                    user.settings.current_realm_id = rid
            elif c == "2":
                user.settings.theme = input("New theme: ").strip() or user.settings.theme
            elif c == "3":
                pref = input("Enter WORLD / LOCAL / BOTH: ").strip().upper()
                if pref in TimeDisplayPreference.__members__:
                    user.settings.set_time_display(TimeDisplayPreference[pref])
                else:
                    print("Invalid.")
            elif c == "0":
                return

    # ---------- Characters ----------
    def list_characters(self) -> None:
        user = self.require_login()
        if not user:
            return
        if not user.character_ids:
            print("(no characters)")
            return
        for cid in user.character_ids:
            ch = self.characters.get(cid)
            if ch:
                print(f"- {cid}: {ch.name} ({ch.class_name}) lvl {ch.level} inv={len(ch.inventory)}")

    def create_character(self) -> None:
        user = self.require_login()
        if not user:
            return
        cid = self._new_id("char", "C")
        name = input("Character name: ").strip()
        cls = input("Class: ").strip()
        level = _safe_int("Level (>=1): ", 1, None)
        ch = Character(char_id=cid, name=name or cid, class_name=cls or "Adventurer", level=level)
        self.characters[cid] = ch
        user.character_ids.append(cid)
        print(f"Created character {cid}: {ch.name}")

    def edit_character_inventory(self) -> None:
        user = self.require_login()
        if not user:
            return
        cid = _pick_from_list("Pick character:", [(cid, f"{cid} {self.characters[cid].name}") for cid in user.character_ids if cid in self.characters])
        if not cid:
            return
        ch = self.characters[cid]
        while True:
            print(f"\n--- Inventory for {ch.name} ({cid}) ---")
            if not ch.inventory:
                print("(empty)")
            else:
                for i, it in enumerate(ch.inventory, start=1):
                    print(f"{i}. {it.name} (type={it.type}, rarity={it.rarity}) - {it.description}")
            print("1) Add item")
            print("2) Remove item by name")
            print("0) Back")
            c = input("Choose: ").strip()
            if c == "1":
                nm = input("Item name: ").strip()
                desc = input("Description: ").strip()
                tp = input("Type: ").strip() or "misc"
                rar = _safe_int("Rarity (int): ", 0, None)
                ch.add_item(InventoryItem(name=nm, description=desc, type=tp, rarity=rar))
            elif c == "2":
                nm = input("Item name to remove: ").strip()
                qty = _safe_int("Qty: ", 1, None)
                removed = ch.remove_item_by_name(nm, qty)
                print(f"Removed {removed}")
            elif c == "0":
                return

    # ---------- Campaigns ----------
    def list_my_campaigns(self) -> None:
        user = self.require_login()
        if not user:
            return
        if not user.campaign_ids:
            print("(no campaigns)")
            return
        for cid in user.campaign_ids:
            c = self.campaigns.get(cid)
            if c:
                print(f"- {cid}: {c.name} vis={c.visibility.value} archived={c.archived} events={len(c.quest_event_ids)}")

    def list_visible_campaigns(self) -> None:
        user = self.require_login()
        if not user:
            return
        visible = []
        for cid, camp in self.campaigns.items():
            if camp.can_view(user.username):
                visible.append((cid, camp))
        if not visible:
            print("(no visible campaigns)")
            return
        for cid, camp in visible:
            owner = camp.owner_username
            print(f"- {cid}: {camp.name} owner={owner} vis={camp.visibility.value} archived={camp.archived}")

    def create_campaign(self) -> None:
        user = self.require_login()
        if not user:
            return
        cid = self._new_id("campaign", "P")
        name = input("Campaign name: ").strip() or cid
        camp = Campaign(campaign_id=cid, owner_username=user.username, name=name)
        self.campaigns[cid] = camp
        user.campaign_ids.append(cid)
        print(f"Created campaign {cid}: {camp.name}")

    def _pick_campaign_i_can_view(self, user: User) -> Optional[str]:
        items = []
        for cid, camp in self.campaigns.items():
            if camp.can_view(user.username):
                items.append((cid, f"{cid} {camp.name} (owner={camp.owner_username}, vis={camp.visibility.value})"))
        return _pick_from_list("Pick a campaign you can view:", items)

    def _pick_campaign_i_can_edit(self, user: User) -> Optional[str]:
        items = []
        for cid, camp in self.campaigns.items():
            if camp.can_edit(user.username):
                items.append((cid, f"{cid} {camp.name} (owner={camp.owner_username}, vis={camp.visibility.value})"))
        return _pick_from_list("Pick a campaign you can edit:", items)

    def edit_campaign(self) -> None:
        user = self.require_login()
        if not user:
            return
        cid = self._pick_campaign_i_can_edit(user)
        if not cid:
            return
        camp = self.campaigns[cid]
        while True:
            print(f"\n--- Campaign {cid}: {camp.name} ---")
            print(f"Owner: {camp.owner_username} | Visibility: {camp.visibility.value} | Archived: {camp.archived}")
            print(f"Shares: {[(s.shared_with_user, s.permission.value) for s in camp.shares]}")
            print("1) Rename")
            print("2) Set visibility (PUBLIC/PRIVATE)")
            print("3) Archive / Unarchive")
            print("4) Share campaign")
            print("5) Unshare campaign")
            print("6) Manage events in this campaign")
            print("7) View timeline (DAY/WEEK/MONTH/YEAR)")
            print("0) Back")
            c = input("Choose: ").strip()
            if c == "1":
                camp.name = input("New name: ").strip() or camp.name
            elif c == "2":
                v = input("Enter PUBLIC or PRIVATE: ").strip().upper()
                if v in Visibility.__members__:
                    camp.visibility = Visibility[v]
                else:
                    print("Invalid.")
            elif c == "3":
                camp.archived = not camp.archived
            elif c == "4":
                self._share_campaign(camp)
            elif c == "5":
                self._unshare_campaign(camp)
            elif c == "6":
                self.manage_events(camp)
            elif c == "7":
                self.view_timeline(camp)
            elif c == "0":
                return

    def _share_campaign(self, camp: Campaign) -> None:
        if not self.users:
            print("No users exist.")
            return
        to_user = input("Share with username: ").strip()
        if to_user not in self.users:
            print("User not found.")
            return
        p = input("Permission (VIEW_ONLY/COLLABORATIVE): ").strip().upper()
        if p not in PermissionLevel.__members__:
            print("Invalid permission.")
            return
        camp.share_with(to_user, PermissionLevel[p])
        print("Shared.")

    def _unshare_campaign(self, camp: Campaign) -> None:
        to_user = input("Unshare with username: ").strip()
        camp.unshare_with(to_user)
        print("Unshared (if existed).")

    # ---------- Events ----------
    def manage_events(self, camp: Campaign) -> None:
        user = self.require_login()
        if not user:
            return
        if not camp.can_edit(user.username):
            print("You do not have edit permission for this campaign.")
            return

        while True:
            print(f"\n--- Events in Campaign {camp.campaign_id}: {camp.name} ---")
            if not camp.quest_event_ids:
                print("(no events)")
            else:
                for eid in camp.quest_event_ids:
                    e = self.events.get(eid)
                    if e:
                        realm = self.realms.get(e.realm_id)
                        rname = realm.name if realm else e.realm_id
                        print(f"- {eid}: {e.name} [{e.start_time}] realm={rname} shares={len(e.shares)} participants={len(e.participant_char_ids)}")
            print("1) Add event")
            print("2) Edit event")
            print("3) Remove event")
            print("0) Back")
            c = input("Choose: ").strip()
            if c == "1":
                self.add_event_to_campaign(camp)
            elif c == "2":
                self.edit_event(camp)
            elif c == "3":
                self.remove_event_from_campaign(camp)
            elif c == "0":
                return

    def add_event_to_campaign(self, camp: Campaign) -> None:
        eid = self._new_id("event", "E")
        name = input("Event name: ").strip() or eid
        start = _parse_time("START")
        end_opt = input("Has end time? (y/n): ").strip().lower()
        end = _parse_time("END") if end_opt == "y" else None

        rid = _pick_from_list("Pick realm:", [(r.realm_id, f"{r.realm_id} {r.name} (offset {r.time_rule.offset_minutes}m)") for r in self.realms.values()])
        if not rid:
            print("Cancelled.")
            return

        e = QuestEvent(event_id=eid, name=name, start_time=start, end_time=end, realm_id=rid)
        self.events[eid] = e
        camp.quest_event_ids.append(eid)
        print(f"Added event {eid}")

        self._edit_event_participants(e)
        self._edit_event_inventory_changes(e)

    def remove_event_from_campaign(self, camp: Campaign) -> None:
        eid = _pick_from_list("Pick event:", [(eid, f"{eid} {self.events[eid].name}") for eid in camp.quest_event_ids if eid in self.events])
        if not eid:
            return
        camp.quest_event_ids.remove(eid)
        # keep event in global store (optional) — but removing globally is fine too.
        # We'll delete globally to simplify.
        if eid in self.events:
            del self.events[eid]
        print("Removed.")

    def edit_event(self, camp: Campaign) -> None:
        eid = _pick_from_list("Pick event:", [(eid, f"{eid} {self.events[eid].name}") for eid in camp.quest_event_ids if eid in self.events])
        if not eid:
            return
        e = self.events[eid]
        while True:
            realm = self.realms.get(e.realm_id)
            rname = realm.name if realm else e.realm_id
            print(f"\n--- Event {eid}: {e.name} ---")
            print(f"Start: {e.start_time} | End: {e.end_time if e.end_time else '(none)'} | Realm: {rname}")
            print(f"Participants: {e.participant_char_ids}")
            print(f"Shares: {[(s.shared_with_user, s.permission.value) for s in e.shares]}")
            print(f"InventoryChanges: {[(chg.item.name, chg.delta_qty, chg.target_char_id) for chg in e.inventory_changes]}")
            print("1) Rename")
            print("2) Edit start time")
            print("3) Edit end time")
            print("4) Change realm")
            print("5) Edit participants")
            print("6) Share event")
            print("7) Unshare event")
            print("8) Edit inventory changes")
            print("0) Back")
            c = input("Choose: ").strip()
            if c == "1":
                e.name = input("New name: ").strip() or e.name
            elif c == "2":
                e.start_time = _parse_time("START")
            elif c == "3":
                yn = input("Set end time? (y to set / n to clear): ").strip().lower()
                e.end_time = _parse_time("END") if yn == "y" else None
            elif c == "4":
                rid = _pick_from_list("Pick realm:", [(r.realm_id, f"{r.realm_id} {r.name}") for r in self.realms.values()])
                if rid:
                    e.realm_id = rid
            elif c == "5":
                self._edit_event_participants(e)
            elif c == "6":
                self._share_event(e)
            elif c == "7":
                self._unshare_event(e)
            elif c == "8":
                self._edit_event_inventory_changes(e)
            elif c == "0":
                return

    def _edit_event_participants(self, e: QuestEvent) -> None:
        user = self.require_login()
        if not user:
            return
        # participants should generally be from the owner's characters,
        # but to keep it simple we allow current user's characters.
        while True:
            print("\nParticipants:")
            print(e.participant_char_ids if e.participant_char_ids else "(none)")
            print("1) Add participant")
            print("2) Remove participant")
            print("0) Done")
            c = input("Choose: ").strip()
            if c == "1":
                cid = _pick_from_list("Pick character:", [(cid, f"{cid} {self.characters[cid].name}") for cid in user.character_ids if cid in self.characters])
                if cid and cid not in e.participant_char_ids:
                    e.participant_char_ids.append(cid)
            elif c == "2":
                cid = _pick_from_list("Pick to remove:", [(cid, cid) for cid in e.participant_char_ids])
                if cid and cid in e.participant_char_ids:
                    e.participant_char_ids.remove(cid)
            elif c == "0":
                return

    def _edit_event_inventory_changes(self, e: QuestEvent) -> None:
        while True:
            print("\nInventory changes:")
            if not e.inventory_changes:
                print("(none)")
            else:
                for i, chg in enumerate(e.inventory_changes, start=1):
                    print(f"{i}. item={chg.item.name} delta={chg.delta_qty} target={chg.target_char_id}")
            print("1) Add change")
            print("2) Remove change")
            print("3) Apply changes now")
            print("0) Done")
            c = input("Choose: ").strip()
            if c == "1":
                item_name = input("Item name: ").strip()
                desc = input("Description: ").strip()
                tp = input("Type: ").strip() or "misc"
                rar = _safe_int("Rarity (int): ", 0, None)
                delta = _safe_int("Delta qty (+grant / -remove): ", -10**9, 10**9)
                target = input("Target character id (blank = all participants): ").strip() or None
                e.inventory_changes.append(InventoryChange(
                    item=InventoryItem(name=item_name, description=desc, type=tp, rarity=rar),
                    delta_qty=delta,
                    target_char_id=target
                ))
            elif c == "2":
                if not e.inventory_changes:
                    continue
                idx = _safe_int("Index to remove: ", 1, len(e.inventory_changes))
                e.inventory_changes.pop(idx - 1)
            elif c == "3":
                self._apply_event_inventory_changes(e)
            elif c == "0":
                return

    def _apply_event_inventory_changes(self, e: QuestEvent) -> None:
        # Apply to target_char_id or all participants
        for chg in e.inventory_changes:
            targets: List[str]
            if chg.target_char_id:
                targets = [chg.target_char_id]
            else:
                targets = list(e.participant_char_ids)

            for cid in targets:
                ch = self.characters.get(cid)
                if not ch:
                    continue
                if chg.delta_qty > 0:
                    for _ in range(chg.delta_qty):
                        ch.add_item(chg.item)
                elif chg.delta_qty < 0:
                    ch.remove_item_by_name(chg.item.name, qty=-chg.delta_qty)
        print("Applied inventory changes.")

    def _share_event(self, e: QuestEvent) -> None:
        to_user = input("Share event with username: ").strip()
        if to_user not in self.users:
            print("User not found.")
            return
        p = input("Permission (VIEW_ONLY/COLLABORATIVE): ").strip().upper()
        if p not in PermissionLevel.__members__:
            print("Invalid permission.")
            return
        e.share_with(to_user, PermissionLevel[p])
        print("Shared event.")

    def _unshare_event(self, e: QuestEvent) -> None:
        to_user = input("Unshare event with username: ").strip()
        e.unshare_with(to_user)
        print("Unshared event (if existed).")

    # ---------- Timeline / Views ----------
    def view_timeline(self, camp: Campaign) -> None:
        user = self.require_login()
        if not user:
            return
        if not camp.can_view(user.username):
            print("You cannot view this campaign.")
            return

        r = input("Range (DAY/WEEK/MONTH/YEAR): ").strip().upper()
        if r not in TimeRangeType.__members__:
            print("Invalid range.")
            return
        anchor = _parse_time("ANCHOR (used as start day 00:00)")

        events = self._get_campaign_events_by_range(camp, TimeRangeType[r], anchor)
        print(f"\n--- Timeline {TimeRangeType[r].value} for {camp.name} (anchor {anchor}) ---")
        if not events:
            print("(no events in range)")
            return

        for e in events:
            # permission: campaign permission OR event share permission (event share lets user see that event alone)
            # Here: since we're in a campaign view, user can already view campaign.
            realm = self.realms.get(e.realm_id)
            realm_name = realm.name if realm else e.realm_id

            world_str = str(e.start_time)
            local_str = str(realm.time_rule.to_local(e.start_time)) if realm else world_str

            if user.settings.time_display == TimeDisplayPreference.WORLD:
                t = world_str
            elif user.settings.time_display == TimeDisplayPreference.LOCAL:
                t = f"{local_str} ({realm_name})"
            else:
                t = f"{world_str} | {local_str} ({realm_name})"

            print(f"- {e.event_id}: {e.name} @ {t}")

    def _get_campaign_events_by_range(self, camp: Campaign, range_type: TimeRangeType, anchor: WorldClockTime) -> List[QuestEvent]:
        start_day_minutes = anchor.day * 24 * 60  # simple
        if range_type == TimeRangeType.DAY:
            start = start_day_minutes
            end = start + 24 * 60
        elif range_type == TimeRangeType.WEEK:
            start = start_day_minutes
            end = start + 7 * 24 * 60
        elif range_type == TimeRangeType.MONTH:
            start = start_day_minutes
            end = start + 30 * 24 * 60
        else:  # YEAR
            start = start_day_minutes
            end = start + 365 * 24 * 60

        collected: List[QuestEvent] = []
        for eid in camp.quest_event_ids:
            e = self.events.get(eid)
            if not e:
                continue
            m = e.start_time.to_minutes()
            if start <= m < end:
                collected.append(e)
        collected.sort(key=lambda ev: ev.start_time.to_minutes())
        return collected

    # ---------- Shared Events listing (event share without campaign share) ----------
    def list_events_shared_with_me(self) -> None:
        user = self.require_login()
        if not user:
            return
        found = []
        for e in self.events.values():
            for s in e.shares:
                if s.shared_with_user == user.username:
                    found.append((e, s.permission))
        if not found:
            print("(no events shared with you)")
            return
        print("\n--- Events shared with you ---")
        for e, perm in found:
            realm = self.realms.get(e.realm_id)
            rname = realm.name if realm else e.realm_id
            print(f"- {e.event_id}: {e.name} realm={rname} start={e.start_time} perm={perm.value}")


    def run(self) -> None:
        self.ensure_default_realm()
        while True:
            print("\n==============================")
            print("GuildQuest CLI")
            print("==============================")
            print(f"Current user: {self.current_user if self.current_user else '(none)'}")
            print("1) Create user")
            print("2) Login")
            print("3) Realms (list/create)")
            print("4) Settings")
            print("5) Characters")
            print("6) Campaigns (my/visible/create/edit)")
            print("7) Events shared with me")
            print("8) Save")
            print("9) Load")
            print("0) Exit")
            cmd = input("Choose: ").strip()

            if cmd == "1":
                self.create_user()
            elif cmd == "2":
                self.login()
            elif cmd == "3":
                self.menu_realms()
            elif cmd == "4":
                self.edit_settings()
            elif cmd == "5":
                self.menu_characters()
            elif cmd == "6":
                self.menu_campaigns()
            elif cmd == "7":
                self.list_events_shared_with_me()
            elif cmd == "8":
                self.save()
            elif cmd == "9":
                self.load()
            elif cmd == "0":
                print("Bye!")
                return

    def menu_realms(self) -> None:
        while True:
            print("\n--- Realms ---")
            print("1) List realms")
            print("2) Create realm")
            print("0) Back")
            c = input("Choose: ").strip()
            if c == "1":
                self.list_realms()
            elif c == "2":
                self.create_realm()
            elif c == "0":
                return

    def menu_characters(self) -> None:
        while True:
            print("\n--- Characters ---")
            print("1) List my characters")
            print("2) Create character")
            print("3) Edit inventory")
            print("0) Back")
            c = input("Choose: ").strip()
            if c == "1":
                self.list_characters()
            elif c == "2":
                self.create_character()
            elif c == "3":
                self.edit_character_inventory()
            elif c == "0":
                return

    def menu_campaigns(self) -> None:
        user = self.require_login()
        if not user:
            return
        while True:
            print("\n--- Campaigns ---")
            print("1) List my campaigns")
            print("2) List campaigns visible to me (public/shared)")
            print("3) Create campaign")
            print("4) Edit a campaign (if I can edit)")
            print("0) Back")
            c = input("Choose: ").strip()
            if c == "1":
                self.list_my_campaigns()
            elif c == "2":
                self.list_visible_campaigns()
            elif c == "3":
                self.create_campaign()
            elif c == "4":
                self.edit_campaign()
            elif c == "0":
                return


if __name__ == "__main__":
    app = GuildQuestApp()
    app.load()  # auto-load if file exists, otherwise ignore
    app.run()
