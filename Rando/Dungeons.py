from typing import TYPE_CHECKING

from Options import OptionError
from Fill import FillError

from ..Locations import LOCATION_TABLE
from ..Items import ITEM_TABLE
from ..Options import SSOptions
from ..Constants import *

if TYPE_CHECKING:
    from .. import SSWorld


class DungeonRando:
    """
    Class handles required dungeons.
    """

    def __init__(self, world: "SSWorld"):
        self.world = world
        self.multiword = world.multiworld

        self.required_dungeons: list[str] = []
        self.banned_dungeons: list[str] = []
        self.required_dungeon_checks: list[str] = []

    def randomize_required_dungeons(self) -> None:
        """
        Randomize required dungeons based on player's options
        """

        self.num_required_dungeons = self.world.options.required_dungeon_count.value

        if self.num_required_dungeons > 6 or self.num_required_dungeons < 0:
            raise OptionError("Required dungeon count must be between 0 and 6.")

        # Randomize required dungeons
        self.required_dungeons.extend(
            self.multiword.random.sample(
                list(DUNGEON_FINAL_CHECKS.keys()), self.num_required_dungeons
            )
        )
        self.required_dungeons = sorted(self.required_dungeons, key=lambda i: DUNGEON_LIST.index(i))

        self.required_dungeon_checks.extend(
            [
                chk
                for dun, chk in DUNGEON_FINAL_CHECKS.items()
                if dun in self.required_dungeons
            ]
        )
        
        self.banned_dungeons.extend(
            [
                dun
                for dun in DUNGEON_FINAL_CHECKS.keys()
                if dun not in self.required_dungeons
            ]
        )
        self.required_dungeons = sorted(self.required_dungeons, key=lambda i: DUNGEON_LIST.index(i))


class DungeonKeyHandler:
    """
    Class handles key placement for dungeon maps, small keys, and boss keys.
    """

    def __init__(self, world: "SSWorld"):
        self.world = world
        self.multiworld = world.multiworld

        self.all_maps: dict[str, str] = {}
        self.all_skeys: dict[str, list] = {}
        self.all_bkeys: dict[str, str] = {}

        self.map_placement: dict[str, str] = {}
        self.skey_placement: dict[str, str] = {}
        self.bkey_placement: dict[str, str] = {}

        for dun in DUNGEON_LIST:
            self.all_maps[dun] = f"{dun} Map"
            self.all_skeys[dun] = [f"{dun} Small Key"] * ITEM_TABLE[f"{dun} Small Key"].quantity
            if dun != "Sky Keep":
                self.all_bkeys[dun] = f"{dun} Boss Key"
        
    def place_dungeon_maps(self) -> list[str]:
        """
        Places dungeon maps based on options.
        """
        items_to_place = list(self.all_maps.values())
        placed = []
        if self.world.options.map_mode == "start_with":
            raise FillError("Tried to place maps, but option is start with.")
        elif self.world.options.map_mode == "vanilla":
            return [] # TODO
        elif self.world.options.map_mode == "own_dungeon":
            locs_placeable = []
            for dun in self.all_maps.keys():
                for loc in self.world.get_locations():
                    if loc.parent_region == dun and loc.item is None:
                        locs_placeable.append(tuple(loc.name, loc.player))
        elif self.world.options.map_mode == "own_dungeon_any_world":
            locs_placeable = []
            for dun in self.all_maps.keys():
                for loc in self.multiworld.get_locations():
                    if loc.game != "Skyward Sword":
                        continue
                    elif loc.parent_region == dun and loc.item is None:
                        locs_placeable.append(tuple(loc.name, loc.player))
        elif self.world.options.map_mode == "anywhere":
            return []
        for map_item in items_to_place:
            loc_to_place = self.world.random.choice(locs_placeable)
            self.multiworld.worlds[loc_to_place[1]].get_location(loc_to_place[0]).place_locked_item(map_item)
            locs_placeable.remove(loc_to_place)
            placed.append(map_item)

        return placed
    
    def place_small_keys(self) -> list[str]:
        """
        Places small keys based on options.
        """
        items_to_place = list(self.all_skeys.values())
        placed = []
        if self.world.options.small_key_mode == "vanilla":
            self.world.get_location("Lanayru Caves - Golo's Gift").place_locked_item("Lanayru Caves Small Key")
            placed.append("Lanayru Caves Small Key")
            return [] # TODO
        elif self.world.options.small_key_mode == "own_dungeon":
            locs_placeable = []
            for dun in self.all_skeys.keys():
                for loc in self.world.get_locations():
                    if loc.parent_region == dun and loc.item is None:
                        locs_placeable.append(tuple(loc.name, loc.player))
            self.world.get_location("Lanayru Caves - Golo's Gift").place_locked_item("Lanayru Caves Small Key")
            placed.append("Lanayru Caves Small Key")
        elif self.world.options.small_key_mode == "own_dungeon_any_world":
            locs_placeable = []
            for dun in self.all_skeys.keys():
                for loc in self.multiworld.get_locations():
                    if loc.game != "Skyward Sword":
                        continue
                    elif loc.parent_region == dun and loc.item is None:
                        locs_placeable.append(tuple(loc.name, loc.player))
            self.world.get_location("Lanayru Caves - Golo's Gift").place_locked_item("Lanayru Caves Small Key")
            placed.append("Lanayru Caves Small Key")
        elif self.world.options.small_key_mode == "lanayru_caves_key_only":
            locs_placeable = []
            for dun in self.all_skeys.keys():
                for loc in self.multiworld.get_locations():
                    if loc.game != "Skyward Sword":
                        continue
                    elif loc.parent_region == dun and loc.item is None:
                        locs_placeable.append(tuple(loc.name, loc.player))
        elif self.world.options.small_key_mode == "anywhere":
            return []
        for skey_item in items_to_place:
            loc_to_place = self.world.random.choice(locs_placeable)
            self.multiworld.worlds[loc_to_place[1]].get_location(loc_to_place[0]).place_locked_item(skey_item)
            locs_placeable.remove(loc_to_place)
            placed.append(skey_item)

        return placed

    def place_boss_keys(self) -> list[str]:
        """
        Places boss keys based on options.
        """
        items_to_place = list(self.all_bkeys.values())
        placed = []
        if self.world.options.boss_key_mode == "vanilla":
            return [] # TODO
        elif self.world.options.boss_key_mode == "own_dungeon":
            locs_placeable = []
            for dun in self.all_bkeys.keys():
                for loc in self.world.get_locations():
                    if loc.parent_region == dun and loc.item is None:
                        locs_placeable.append(tuple(loc.name, loc.player))
        elif self.world.options.boss_key_mode == "own_dungeon_any_world":
            locs_placeable = []
            for dun in self.all_bkeys.keys():
                for loc in self.multiworld.get_locations():
                    if loc.game != "Skyward Sword":
                        continue
                    elif loc.parent_region == dun and loc.item is None:
                        locs_placeable.append(tuple(loc.name, loc.player))
        elif self.world.options.boss_key_mode == "anywhere":
            return []
        for bkey_item in items_to_place:
            loc_to_place = self.world.random.choice(locs_placeable)
            self.multiworld.worlds[loc_to_place[1]].get_location(loc_to_place[0]).place_locked_item(bkey_item)
            locs_placeable.remove(loc_to_place)
            placed.append(bkey_item)

        return placed
