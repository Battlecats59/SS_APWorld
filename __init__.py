import os
from base64 import b64encode
from collections.abc import Mapping
from dataclasses import fields
from typing import Any, ClassVar

import yaml

from BaseClasses import MultiWorld, Region, Tutorial
from Options import Toggle
from worlds.AutoWorld import WebWorld, World
from worlds.generic.Rules import add_item_rule
from worlds.LauncherComponents import (
    Component,
    SuffixIdentifier,
    Type,
    components,
    launch_subprocess,
)

from .Constants import *

from .Macros import *
from .Items import ITEM_TABLE, SSItem
from .Locations import LOCATION_TABLE, SSLocation, SSLocFlag
from .Options import SSOptions
from .Rules import set_rules
from .Names import HASH_NAMES

from .Rando.Dungeons import DungeonRando
from .Rando.Entrances import EntranceRando
from .Rando.ItemPlacement import handle_itempool, item_classification
from .Rando.HintPlacement import handle_hints

AP_VERSION = [0, 5, 1]
WORLD_VERSION = [0, 1, 0]
RANDO_VERSION = [2, 2, 0]

def run_client() -> None:
    """
    Launch the Skyward Sword client.
    """
    print("Running SS Client")
    from .SSClient import main

    launch_subprocess(main, name="SSClient")


components.append(
    Component(
        "Skyward Sword Client",
        func=run_client,
        component_type=Type.CLIENT,
        file_identifier=SuffixIdentifier(".apssr"),
    )
)


class SSWorld(World):
    """
    What if that's Zelda down there, and she's sending me a signal? It's a sign!
    It says, `Save me, Groose. You're my only hope!`
    The more I think about it, the more sure I get! It's Zelda down there, and I gotta go rescue her!

    Anyhow, don't think about trying to go down there before me. I'm her hero, remember?

    Ugh. I don't even know why I'm talking to you. Looking at you just makes me feel sad again.
    """

    options_dataclass = SSOptions
    options: SSOptions

    game: ClassVar[str] = "Skyward Sword"
    topology_present: bool = True
    required_client_version: tuple[int, int, int] = (0, 5, 1)
    origin_region_name: str = "Upper Skyloft"

    item_name_to_id: ClassVar[dict[str, int]] = {
        name: SSItem.get_apid(data.code) for name, data in ITEM_TABLE.items() if data.code is not None
    }
    location_name_to_id: ClassVar[dict[str, int]] = {
        name: SSLocation.get_apid(data.code) for name, data in LOCATION_TABLE.items() if data.code is not None
    }

    create_items = handle_itempool
    set_rules = set_rules

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.progress_locations: set[str] = set()
        self.nonprogress_locations: set[str] = set()

        self.dungeons = DungeonRando(self)
        self.entrances = EntranceRando(self)

    def determine_progress_and_nonprogress_locations(self) -> tuple[set[str], set[str]]:
        """
        Determine which locations are progress or nonprogress based on player's options.

        :return: A tuple of a set of progress locations and a set of nonprogress locations.
        """

        progress_locations: set[str] = set()
        nonprogress_locations: set[str] = set()

        def add_flag(option: Toggle, flag: SSLocFlag) -> SSLocFlag:
            return flag if option else SSLocFlag.ALWAYS

        for loc, data in LOCATION_TABLE.items():
            progress_locations.add(loc)
            # For now, every location is progress

        return progress_locations, nonprogress_locations

    def generate_early(self) -> None:
        """
        Run before any other steps of the multiworld, but after options.
        """

        self.progress_locations, self.nonprogress_locations = (
            self.determine_progress_and_nonprogress_locations()
        )

    def create_regions(self) -> None:
        """
        Create and connect regions.
        """

        def get_access_rule(region: str) -> str:
            formatted_region = region.lower().replace("'", "").replace(" ", "_")
            return f"can_access_{formatted_region}"

        for reg in OVERWORLD_REGIONS.keys():
            apreg = Region(reg, self.player, self.multiworld)
            self.multiworld.regions.append(apreg)

        for reg, conn in OVERWORLD_REGIONS.items():
            for conn_reg in conn:
                self.get_region(reg).connect(
                    self.get_region(conn_reg),
                    rule=lambda state, region=conn_reg: getattr(
                        Macros, get_access_rule(region)
                    )(state, self.player),
                )

        self.dungeons.randomize_required_dungeons()
        self.entrances.randomize_dungeon_entrances(self.dungeons.required_dungeons)
        self.entrances.randomize_trial_gates()

        for dun, conn in self.entrances.dungeon_connections.items():
            if conn == "dungeon_entrance_in_deep_woods":
                dun_entrance_region = "Faron Woods"
            elif conn == "dungeon_entrance_in_lake_floria":
                dun_entrance_region = "Lake Floria"
            elif conn == "dungeon_entrance_in_eldin_volcano":
                dun_entrance_region = "Eldin Volcano"
            elif conn == "dungeon_entrance_in_volcano_summit":
                dun_entrance_region = "Volcano Summit"
            elif conn == "dungeon_entrance_in_lanayru_desert":
                dun_entrance_region = "Lanayru Desert"
            elif conn == "dungeon_entrance_in_lanayru_sand_sea":
                dun_entrance_region = "Lanayru Sand Sea"
            elif conn == "dungeon_entrance_on_skyloft":
                dun_entrance_region = "Central Skyloft"

            apreg = Region(dun, self.player, self.multiworld)
            apreg.connect(self.get_region(dun_entrance_region))
            self.multiworld.regions.append(apreg)

            self.get_region(dun_entrance_region).connect(
                apreg,
                rule=lambda state, entrance=conn: getattr(
                    Macros, f"can_reach_{entrance}"
                ),
            )

        for trl, conn in self.entrances.trial_connections.items():
            if conn == "trial_gate_on_skyloft":
                trl_gate_region = "Central Skyloft"
            elif conn == "trial_gate_in_faron_woods":
                trl_gate_region = "Faron Woods"
            elif conn == "trial_gate_in_eldin_volcano":
                trl_gate_region = "Eldin Volcano"
            elif conn == "trial_gate_in_lanayru_desert":
                trl_gate_region = "Lanayru Desert"

            apreg = Region(trl, self.player, self.multiworld)
            apreg.connect(self.get_region(trl_gate_region))
            self.multiworld.regions.append(apreg)

            self.get_region(trl_gate_region).connect(
                apreg, rule=lambda state, gate=conn: getattr(Macros, f"can_open_{gate}")
            )

        # Place locations within the regions
        for loc in self.progress_locations:
            loc_data = LOCATION_TABLE[loc]

            loc_region = self.get_region(loc_data.region)
            location = SSLocation(self.player, loc, loc_region, loc_data)
            loc_region.locations.append(location)

    def create_item(self, name: str) -> SSItem:
        """
        Create an item for the Skyward Sword world for this player.

        :param name: The name of the item.
        :raises KeyError: If an invalid item name is provided.
        """

        if name in ITEM_TABLE:
            return SSItem(
                name, self.player, ITEM_TABLE[name], item_classification(self, name)
            )
        raise KeyError(f"Invalid item name: {name}")

    def generate_output(self, output_directory: str) -> None:
        """
        Create the output .apssr file that is used to randomize the ISO.

        :param output_directory: The output directory for the .apssr file.
        """
        multiworld = self.multiworld
        player = self.player
        player_hash = self.multiworld.per_slot_randoms[player].sample(HASH_NAMES, 3)

        # Output seed name and slot number to seed RNG in randomizer client.
        output_data = {
            "AP Version": list(AP_VERSION),
            "World Version": list(WORLD_VERSION),
            "Hash": f"AP P{player} " + " ".join(player_hash),
            "AP Seed": multiworld.seed_name,
            "Rando Seed": self.multiworld.per_slot_randoms[player].randint(0, 2**32 - 1),
            "Slot": player,
            "Name": self.player_name,
            "Options": {},
            "Starting Items": self.starting_items,
            "Required Dungeons": self.dungeons.required_dungeons,
            "Locations": {},
            "Hints": handle_hints(self),
            "Dungeon Entrances": {},
            "Trial Entrances": {},
        }

        # Output options to file.
        for field in fields(self.options):
            output_data["Options"][field.name.replace("_", "-")] = getattr(
                self.options, field.name
            ).value

        # Output which item has been placed at each location.
        locations = multiworld.get_locations(player)
        for location in locations:
            if location.name != "Hylia's Realm - Defeat Demise":
                if location.item:
                    item_info = {
                        "player": location.item.player,
                        "name": location.item.name,
                        "game": location.item.game,
                        "classification": location.item.classification.name,
                        "chest_dowsing": 8,
                    }
                else:
                    print(f"No item in location: {location.name}. Defaulting to red rupee.")
                    item_info = {
                        "player": location.item.player,
                        "name": "Red Rupee",
                        "game": "Skyward Sword",
                        "classification": "filler",
                        "chest_dowsing": 8,
                    }
                output_data["Locations"][location.name] = item_info

        # Fix entrances
        dunconn = {}
        trlconn = {}
        for dun, ent in self.entrances.dungeon_connections.items():
            rando_friendly_entrance_name_list = []
            for w in ent.split("_"):
                if w not in ["in", "on"]:
                    w = w[0].upper() + w[1:]
                rando_friendly_entrance_name_list.append(w)
            rando_friendly_entrance_name = " ".join(rando_friendly_entrance_name_list)
            dunconn[rando_friendly_entrance_name] = dun
        for dun in sorted(dunconn.keys(), key=lambda i: DUNGEON_ENTRANCE_LIST.index(i)):
            output_data["Dungeon Entrances"][dun] = dunconn[dun]
        for trl, gate in self.entrances.trial_connections.items():
            rando_friendly_gate_name_list = []
            for w in gate.split("_"):
                if w not in ["in", "on"]:
                    w = w[0].upper() + w[1:]
                rando_friendly_gate_name_list.append(w)
            rando_friendly_gate_name = " ".join(rando_friendly_gate_name_list)
            trlconn[rando_friendly_gate_name] = trl
        for trl in sorted(trlconn.keys(), key=lambda i: TRIAL_GATE_LIST.index(i)):
            output_data["Trial Entrances"][trl] = trlconn[trl]
        

        # Output the plando details to file.
        file_path = os.path.join(
            output_directory, f"{multiworld.get_out_file_name_base(player)}.apssr"
        )
        with open(file_path, "wb") as f:
            f.write(
                b64encode(bytes(yaml.safe_dump(output_data, sort_keys=False), "utf-8"))
            )

    def fill_slot_data(self) -> Mapping[str, Any]:
        """
        Return the `slot_data` field that will be in the `Connected` network package.

        This is a way the generator can give custom data to the client.
        The client will receive this as JSON in the `Connected` response.

        :return: A dictionary to be sent to the client when it connects to the server.
        """
        slot_data = {
            "required_dungeon_count": self.options.required_dungeon_count.value,
            "triforce_required": self.options.triforce_required.value,
            "triforce_shuffle": self.options.triforce_shuffle.value,
            "got_sword_requirement": self.options.got_sword_requirement.value,
            "got_dungeon_requirement": self.options.got_dungeon_requirement.value,
            "imp2_skip": self.options.imp2_skip.value,
            "skip_horde": self.options.skip_horde.value,
            "skip_g3": self.options.skip_g3.value,
            "skip_demise": self.options.skip_demise.value,
            "got_start": self.options.got_start.value,
            "open_thunderhead": self.options.open_thunderhead.value,
            "open_et": self.options.open_et.value,
            "open_lmf": self.options.open_lmf.value,
            "open_lake_floria": self.options.open_lake_floria.value,
            "empty_unrequired_dungeons": self.options.empty_unrequired_dungeons.value,
            "map_mode": self.options.map_mode.value,
            "small_key_mode": self.options.small_key_mode.value,
            "boss_key_mode": self.options.boss_key_mode.value,
            "fs_lava_flow": self.options.fs_lava_flow.value,
            "shuffle_trial_objects": self.options.shuffle_trial_objects.value,
            "treasuresanity_in_silent_realms": self.options.treasuresanity_in_silent_realms.value,
            "trial_treasure_amount": self.options.trial_treasure_amount.value,
            "randomize_entrances": self.options.randomize_entrances.value,
            "randomize_trials": self.options.randomize_trials.value,
            "random_start_entrance": self.options.random_start_entrance.value,
            "limit_start_entrance": self.options.limit_start_entrance.value,
            "random_start_statues": self.options.random_start_statues.value,
            "shopsanity": self.options.shopsanity.value,
            "rupoor_mode": self.options.rupoor_mode.value,
            "rupeesanity": self.options.rupeesanity.value,
            "tadtonesanity": self.options.tadtonesanity.value,
            "gondo_upgrades": self.options.gondo_upgrades.value,
            "sword_dungeon_reward": self.options.sword_dungeon_reward.value,
            "randomize_boss_key_puzzles": self.options.randomize_boss_key_puzzles.value,
            "random_puzzles": self.options.random_puzzles.value,
            "peatrice_conversations": self.options.peatrice_conversations.value,
            "demise_count": self.options.demise_count.value,
            "dowsing_after_whitesword": self.options.dowsing_after_whitesword.value,
            "full_wallet_upgrades": self.options.full_wallet_upgrades.value,
            "ammo_availability": self.options.ammo_availability.value,
            "upgraded_skyward_strike": self.options.upgraded_skyward_strike.value,
            "fast_air_meter": self.options.fast_air_meter.value,
            "enable_heart_drops": self.options.enable_heart_drops.value,
            "damage_multiplier": self.options.damage_multiplier.value,
            "starting_sword": self.options.starting_sword.value,
            "starting_tablet_count": self.options.starting_tablet_count.value,
            "starting_crystal_packs": self.options.starting_crystal_packs.value,
            "starting_bottles": self.options.starting_bottles.value,
            "starting_heart_containers": self.options.starting_heart_containers.value,
            "starting_heart_pieces": self.options.starting_heart_pieces.value,
            "starting_tadtones": self.options.starting_tadtones.value,
            "random_starting_item": self.options.random_starting_item.value,
            "start_with_hylian_shield": self.options.start_with_hylian_shield.value,
            "full_starting_wallet": self.options.full_starting_wallet.value,
            "max_starting_bugs": self.options.max_starting_bugs.value,
            "max_starting_treasures": self.options.max_starting_treasures.value,
            "song_hints": self.options.song_hints.value,
            "chest_dowsing": self.options.chest_dowsing.value,
            "dungeon_dowsing": self.options.dungeon_dowsing.value,
            "impa_sot_hint": self.options.impa_sot_hint.value,
            "cube_sots": self.options.cube_sots.value,
            "precise_item": self.options.precise_item.value,
            "starting_items": self.options.starting_items.value,
            "death_link": self.options.death_link.value,
        }

        return slot_data
