from collections.abc import Callable
from typing import TYPE_CHECKING

from BaseClasses import MultiWorld
from worlds.AutoWorld import LogicMixin
from worlds.generic.Rules import set_rule

from .Macros import *

if TYPE_CHECKING:
    from . import SSWorld


class SSLogic(LogicMixin):
    """
    Handles logic in Skyward Sword.

    Methods in this class are to be prefixed with "_ss"
    """

    multiworld: MultiWorld

    def _ss_sword_requirement_met(self, player: int) -> bool:
        return (
            (
                has_goddess_sword(self, player)
                and self.multiworld.worlds[player].options.got_sword_requirement
                == "goddess_sword"
            )
            or (
                has_goddess_longsword(self, player)
                and self.multiworld.worlds[player].options.got_sword_requirement
                == "goddess_longsword"
            )
            or (
                has_goddess_white_sword(self, player)
                and self.multiworld.worlds[player].options.got_sword_requirement
                == "goddess_white_sword"
            )
            or (
                has_master_sword(self, player)
                and self.multiworld.worlds[player].options.got_sword_requirement
                == "master_sword"
            )
            or (
                has_true_master_sword(self, player)
                and self.multiworld.worlds[player].options.got_sword_requirement
                == "true_master_sword"
            )
        )

    def _ss_can_beat_required_dungeons(self, player: int) -> bool:
        req_dungeon_checks = self.multiworld.worlds[
            player
        ].dungeons.required_dungeon_checks
        return all(self.can_reach_location(loc, player) for loc in req_dungeon_checks)
    
    def _ss_option_unrequired_dungeons(self, player: int) -> bool:
        return self.multiworld.worlds[player].options.got_dungeon_requirement == "unrequired"

    def _ss_option_upgraded_skyward_strike(self, player: int) -> bool:
        return self.multiworld.worlds[player].options.upgraded_skyward_strike

    def _ss_option_thunderhead_ballad(self, player: int) -> bool:
        return self.multiworld.worlds[player].options.open_thunderhead == "ballad"

    def _ss_option_thunderhead_open(self, player: int) -> bool:
        return self.multiworld.worlds[player].options.open_thunderhead == "open"

    def _ss_option_no_triforce(self, player: int) -> bool:
        return not self.multiworld.worlds[player].options.triforce_required

    def _ss_option_lake_floria_open(self, player: int) -> bool:
        return self.multiworld.worlds[player].options.open_lake_floria == "open"

    def _ss_option_lake_floria_yerbal(self, player: int) -> bool:
        return (
            self.multiworld.worlds[player].options.open_lake_floria == "talk_to_yerbal"
        )

    def _ss_option_damage_multiplier_under_12(self, player: int) -> bool:
        return self.multiworld.worlds[player].options.damage_multiplier < 12

    def _ss_option_lmf_open(self, player: int) -> bool:
        return self.multiworld.worlds[player].options.open_lmf == "open"

    def _ss_option_lmf_main_node(self, player: int) -> bool:
        return self.multiworld.worlds[player].options.open_lmf == "main_node"

    def _ss_option_shopsanity(self, player: int) -> bool:
        return self.multiworld.worlds[player].options.shopsanity

    def _ss_option_gondo_upgrades(self, player: int) -> bool:
        return self.multiworld.worlds[player].options.gondo_upgrades


def set_rules(world: "SSWorld") -> None:
    """
    Defines logic for locations.
    """

    def set_rule_if_progression(
        loc: str, rule: Callable[[CollectionState], bool]
    ) -> None:
        if loc in world.progress_locations:
            set_rule(world.get_location(loc), rule)

    player = world.player

    ### SKYLOFT
    set_rule_if_progression("Upper Skyloft - Fledge's Gift", lambda state: True)
    set_rule_if_progression("Upper Skyloft - Owlan's Gift", lambda state: True)
    set_rule_if_progression("Upper Skyloft - Sparring Hall Chest", lambda state: True)
    set_rule_if_progression(
        "Upper Skyloft - Ring Knight Academy Bell",
        lambda state: distance_activator(state, player)
        or state.has("Gust Bellows", player),
    )
    set_rule_if_progression(
        "Upper Skyloft - Chest near Goddess Statue", lambda state: True
    )
    set_rule_if_progression(
        "Upper Skyloft - First Goddess Sword Item in Goddess Statue", lambda state: True
    )
    set_rule_if_progression(
        "Upper Skyloft - Second Goddess Sword Item in Goddess Statue",
        lambda state: True,
    )
    set_rule_if_progression(
        "Upper Skyloft - In Zelda's Closet",
        lambda state: state.has("Clawshots", player),
    )
    set_rule_if_progression(
        "Upper Skyloft - Owlan's Crystals",
        lambda state: can_reach_oolo(state, player) and state.has("Scrapper", player),
    )
    set_rule_if_progression(
        "Upper Skyloft - Fledge's Crystals",
        lambda state: has_bottle(state, player)
        and unlocked_endurance_potion(state, player),
    )
    set_rule_if_progression(
        "Upper Skyloft - Item from Cawlin",
        lambda state: state.has("Goddess's Harp", player),
    )
    set_rule_if_progression(
        "Upper Skyloft - Ghost/Pipit's Crystals",
        lambda state: state.has("Cawlin's Letter", player),
    )
    set_rule_if_progression(
        "Upper Skyloft - Pumpkin Archery -- 600 Points",
        lambda state: has_bow(state, player),
    )

    set_rule_if_progression("Central Skyloft - Potion Lady's Gift", lambda state: True)
    set_rule_if_progression(
        "Centra; Skyloft - Repair Gondo's Junk",
        lambda state: state.has("Amber Tablet", player)
        and (
            lanayru_mine_ancient_flower_farming(state, player)
            or lanayru_desert_ancient_flower_farming(state, player)
            or lanayru_desert_ancient_flower_farming_near_main_node(state, player)
            or pirate_stronghold_ancient_flower_farming(state, player)
            or lanayru_gorge_ancient_flower_farming(state, player)
        ),
    )
    set_rule_if_progression("Central Skyloft - Wryna's Crystals", lambda state: True)
    set_rule_if_progression(
        "Central Skyloft - Waterfall Cave First Chest",
        lambda state: can_cut_trees(state, player),
    )
    set_rule_if_progression(
        "Central Skyloft - Waterfall Cave Second Chest",
        lambda state: can_cut_trees(state, player),
    )
    set_rule_if_progression(
        "Central Skyloft - Rupee Waterfall Cave Crawlspace",
        lambda state: can_cut_trees(state, player),
    )
    set_rule_if_progression("Central Skyloft - Parrow's Gift", lambda state: True)
    set_rule_if_progression(
        "Central Skyloft - Parrow's Crystals",
        lambda state: can_save_orielle(state, player),
    )
    set_rule_if_progression(
        "Central Skyloft - Peater/Peatrice's Crystals", lambda state: True
    )
    set_rule_if_progression(
        "Central Skyloft - Item in Bird Nest",
        lambda state: state.has("Clawshots", player)
        and state.has("Gust Bellows", player),
    )
    set_rule_if_progression(
        "Central Skyloft - Shed Chest",
        lambda state: state.has("Water Dragon's Scale", player),
    )
    set_rule_if_progression(
        "Central Skyloft - West Cliff Goddess Chest",
        lambda state: goddess_cube_on_west_great_tree_near_exit(state, player),
    )
    set_rule_if_progression(
        "Central Skyloft - Bazaar Goddess Chest",
        lambda state: goddess_cube_in_ancient_harbour(state, player),
    )
    set_rule_if_progression(
        "Central Skyloft - Shed Goddess Chest",
        lambda state: goddess_cube_on_sand_slide(state, player)
        and state.has("Water Dragon's Scale", player),
    )
    set_rule_if_progression(
        "Central Skyloft - Floating Island Goddess Chest",
        lambda state: goddess_cube_in_lake_floria(state, player)
        and state.has("Clawshots", player),
    )
    set_rule_if_progression(
        "Central Skyloft - Waterfall Goddess Chest",
        lambda state: goddess_cube_in_pirate_stronghold(state, player)
        and state.has("Clawshots", player),
    )

    set_rule_if_progression(
        "Skyloft Village - Mallara's Crystals",
        lambda state: state.has("Gust Bellows", player),
    )
    set_rule_if_progression(
        "Skyloft Village - Bertie's Crystals",
        lambda state: state.has("Baby Rattle", player),
    )
    set_rule_if_progression(
        "Skyloft Village - Sparrot's Crystals",
        lambda state: can_reach_second_part_of_eldin_volcano(state, player)
        and state.has("Clawshots", player)
        and state.has("Scrapper", player),
    )

    set_rule_if_progression(
        "Batreaux's House - 5 Crystals",
        lambda state: five_gratitude_crystals(state, player),
    )
    set_rule_if_progression(
        "Batreaux's House - 10 Crystals",
        lambda state: ten_gratitude_crystals(state, player),
    )
    set_rule_if_progression(
        "Batreaux's House - 30 Crystals",
        lambda state: thirty_gratitude_crystals(state, player),
    )
    set_rule_if_progression(
        "Batreaux's House - 30 Crystals Chest",
        lambda state: thirty_gratitude_crystals(state, player),
    )
    set_rule_if_progression(
        "Batreaux's House - 40 Crystals",
        lambda state: forty_gratitude_crystals(state, player),
    )
    set_rule_if_progression(
        "Batreaux's House - 50 Crystals",
        lambda state: fifty_gratitude_crystals(state, player),
    )
    set_rule_if_progression(
        "Batreaux's House - 70 Crystals",
        lambda state: seventy_gratitude_crystals(state, player),
    )
    set_rule_if_progression(
        "Batreaux's House - 70 Crystals Second Reward",
        lambda state: seventy_gratitude_crystals(state, player),
    )
    set_rule_if_progression(
        "Batreaux's House - 80 Crystals",
        lambda state: eighty_gratitude_crystals(state, player),
    )

    set_rule_if_progression(
        "Beedle's Shop - 300 Rupee Item",
        lambda state: can_access_beedles_shop(state, player)
        and can_afford_300_rupees(state, player)
        and (has_pouch(state, player) or state._ss_option_shopsanity(player)),
    )
    set_rule_if_progression(
        "Beedle's Shop - 600 Rupee Item",
        lambda state: can_access_beedles_shop(state, player)
        and can_afford_600_rupees(state, player)
        and (has_pouch(state, player) or state._ss_option_shopsanity(player)),
    )
    set_rule_if_progression(
        "Beedle's Shop - 1200 Rupee Item",
        lambda state: can_access_beedles_shop(state, player)
        and can_afford_1200_rupees(state, player)
        and (has_pouch(state, player) or state._ss_option_shopsanity(player)),
    )
    set_rule_if_progression(
        "Beedle's Shop - 800 Rupee Item",
        lambda state: can_access_beedles_shop(state, player)
        and can_afford_800_rupees(state, player),
    )
    set_rule_if_progression(
        "Beedle's Shop - 1600 Rupee Item",
        lambda state: can_access_beedles_shop(state, player)
        and can_afford_1600_rupees(state, player),
    )
    set_rule_if_progression(
        "Beedle's Shop - First 100 Rupee Item",
        lambda state: can_access_beedles_shop(state, player),
    )
    set_rule_if_progression(
        "Beedle's Shop - Second 100 Rupee Item",
        lambda state: can_access_beedles_shop(state, player),
    )
    set_rule_if_progression(
        "Beedle's Shop - Third 100 Rupee Item",
        lambda state: can_access_beedles_shop(state, player)
        and can_medium_rupee_farm(state, player),
    )
    set_rule_if_progression(
        "Beedle's Shop - 50 Rupee Item",
        lambda state: can_access_beedles_shop(state, player),
    )
    set_rule_if_progression(
        "Beedle's Shop - 1000 Rupee Item",
        lambda state: can_access_beedles_shop(state, player)
        and can_afford_1000_rupees(state, player),
    )

    set_rule_if_progression("Sky - Lumpy Pumpkin - Chandelier", lambda state: True)
    set_rule_if_progression(
        "Sky - Lumpy Pumpkin - Harp Minigame",
        lambda state: state.has("Goddess's Harp", player)
        and has_bottle(state, player),  # Bottle for soup quest
    )
    set_rule_if_progression(
        "Sky - Kina's Crystals",
        lambda state: state.has("Scrapper", player)
        and has_bottle(state, player)
        and state.can_reach_region("Mogma Turf", player),
    )
    set_rule_if_progression(
        "Sky - Orielle's Crystals", lambda state: can_save_orielle(state, player)
    )
    set_rule_if_progression(
        "Sky - Beedle's Crystals",
        lambda state: can_access_beedles_shop(state, player)
        and state.has("Horned Colossus Beetle", player),
    )
    set_rule_if_progression(
        "Sky - Dodoh's Crystals", lambda state: can_retrieve_party_wheel(state, player)
    )
    set_rule_if_progression(
        "Sky - Fun Fun Island Minigame -- 500 Rupees",
        lambda state: can_retrieve_party_wheel(state, player),
    )
    set_rule_if_progression(
        "Sky - Chest in Breakable Boulder near Fun Fun Island",
        lambda state: state.has("Spiral Charge", player),
    )
    set_rule_if_progression(
        "Sky - Chest in Breakable Boulder near Lumpy Pumpkin",
        lambda state: state.has("Spiral Charge", player),
    )
    set_rule_if_progression(
        "Sky - Bamboo Island Goddess Chest",
        lambda state: goddess_cube_west_of_earth_temple_entrance(state, player),
    )
    set_rule_if_progression(
        "Sky - Goddess Chest on Island next to Bamboo Island",
        lambda state: goddess_cube_near_mogma_turf_entrance(state, player),
    )
    set_rule_if_progression(
        "Sky - Goddess Chest in Cave on Island next to Bamboo Island",
        lambda state: goddess_cube_in_secret_passageway(state, player)
        and state.has("Water Dragon's Scale", player),
    )
    set_rule_if_progression(
        "Sky - Beedle's Island Goddess Chest",
        lambda state: goddess_cube_at_ride_near_temple_of_time(state, player),
    )
    set_rule_if_progression(
        "Sky - Beedle's Island Cage Goddess Chest",
        lambda state: goddess_cube_on_top_on_skyview(state, player)
        and can_access_beedles_shop(state, player),
    )
    set_rule_if_progression(
        "Sky - Northeast Island Goddess Chest behind Bombable Rocks",
        lambda state: goddess_cube_at_lanayru_mine_entrance(state, player)
        and state.has("Bomb Bag", player),
    )
    set_rule_if_progression(
        "Sky - Northeast Island Cage Goddess Chest",
        lambda state: goddess_cube_east_of_earth_temple_entrance(state, player),
    )
    set_rule_if_progression(
        "Sky - Lumpy Pumpkin - Goddess Chest on the Roof",
        lambda state: goddess_cube_in_skyview_spring(state, player),
    )
    set_rule_if_progression(
        "Sky - Lumpy Pumpkin - Outside Goddess Chest",
        lambda state: initial_goddess_cube(state, player),
    )
    set_rule_if_progression(
        "Sky - Goddess Chest on Island Closest to Faron Pillar",
        lambda state: goddess_cube_in_deep_woods(state, player),
    )
    set_rule_if_progression(
        "Sky - Goddess Chest outside Volcanic Island",
        lambda state: goddess_cube_in_sand_oasis(state, player),
    )
    set_rule_if_progression(
        "Sky - Goddess Chest inside Volcanic Island",
        lambda state: goddess_cube_on_east_great_tree_with_clawshot_target(
            state, player
        )
        and state.has("Clawshots", player),
    )
    set_rule_if_progression(
        "Sky - Goddess Chest under Fun Fun Island",
        lambda state: goddess_cube_in_floria_waterfall(state, player),
    )
    set_rule_if_progression(
        "Sky - Southwest Triple Island Upper Goddess Chest",
        lambda state: goddess_cube_at_eldin_entrance(state, player),
    )
    set_rule_if_progression(
        "Sky - Southwest Triple Island Lower Goddess Chest",
        lambda state: goddess_cube_near_caged_robot(state, player),
    )
    set_rule_if_progression(
        "Sky - Southwest Triple Island Cage Goddess Chest",
        lambda state: goddess_cube_in_skippers_retreat(state, player)
        and state.has("Clawshots", player),
    )

    # Thunderhead
    set_rule_if_progression(
        "Thunderhead - Isle of Songs - Strike Crest with Goddess Sword",
        lambda state: can_access_thunderhead(state, player)
        and has_goddess_sword(state, player),
    )
    set_rule_if_progression(
        "Thunderhead - Isle of Songs - Strike Crest with Longsword",
        lambda state: can_access_thunderhead(state, player)
        and has_goddess_longsword(state, player),
    )
    set_rule_if_progression(
        "Thunderhead - Isle of Songs - Strike Crest with White Sword",
        lambda state: can_access_thunderhead(state, player)
        and has_goddess_white_sword(state, player),
    )
    set_rule_if_progression(
        "Thunderhead - Song from Levias",
        lambda state: can_access_thunderhead(state, player)
        and has_practice_sword(state, player)
        and state.has("Scrapper", player)
        and state.has("Spiral Charge", player),
    )
    set_rule_if_progression(
        "Thunderhead - Bug Heaven -- 10 Bugs in 3 Minutes",
        lambda state: can_access_thunderhead(state, player)
        and has_bug_net(state, player),
    )
    set_rule_if_progression(
        "Thunderhead - East Island Chest",
        lambda state: can_access_thunderhead(state, player)
        and has_digging_mitts(state, player),
    )
    set_rule_if_progression(
        "Thunderhead - East Island Goddess Chest",
        lambda state: can_access_thunderhead(state, player)
        and goddess_cube_on_east_great_tree_with_rope(state, player),
    )
    set_rule_if_progression(
        "Thunderhead - Goddess Chest on top of Isle of Songs",
        lambda state: can_access_thunderhead(state, player)
        and goddess_cube_near_fire_sanctuary_entrance(state, player),
    )
    set_rule_if_progression(
        "Thunderhead - Goddess Chest outside Isle of Songs",
        lambda state: can_access_thunderhead(state, player)
        and goddess_cube_in_mogma_turf(state, player),
    )
    set_rule_if_progression(
        "Thunderhead - First Goddess Chest on Mogma Mitts Island",
        lambda state: can_access_thunderhead(state, player)
        and goddess_cube_inside_volcano_summit(state, player)
        and has_mogma_mitts(state, player),
    )
    set_rule_if_progression(
        "Thunderhead - Second Goddess Chest on Mogma Mitts Island",
        lambda state: can_access_thunderhead(state, player)
        and goddess_cube_in_lanayru_gorge(state, player)
        and has_mogma_mitts(state, player),
    )
    set_rule_if_progression(
        "Thunderhead - Bug Heaven Goddess Chest",
        lambda state: can_access_thunderhead(state, player)
        and goddess_cube_in_summit_waterfall(state, player),
    )

    # Sealed Grounds
    set_rule_if_progression(
        "Sealed Grounds - Chest inside Sealed Temple",
        lambda state: can_reach_sealed_temple(state, player),
    )
    set_rule_if_progression(
        "Sealed Grounds - Song from Impa",
        lambda state: can_reach_sealed_temple(state, player)
        and state.has("Goddess's Harp", player),
    )
    set_rule_if_progression(
        "Sealed Grounds - Gorko's Goddess Wall Reward",
        lambda state: can_reach_sealed_temple(state, player)
        and state.has("Goddess's Harp", player)
        and state.has("Ballad of the Goddess", player)
        and has_goddess_sword(state, player),
    )
    set_rule_if_progression(
        "Sealed Grounds - Zelda's Blessing", lambda state: can_reach_past(state, player)
    )

    # Faron Woods
    set_rule_if_progression(
        "Faron Woods - Item behind Lower Bombable Rock",
        lambda state: can_reach_most_of_faron_woods(state, player)
        and state.has("Bomb Bag", player),
    )
    set_rule_if_progression(
        "Faron Woods - Item on Tree",
        lambda state: can_reach_most_of_faron_woods(state, player),
    )
    set_rule_if_progression(
        "Faron Woods - Kikwi Elder's Reward",
        lambda state: can_reach_most_of_faron_woods(state, player)
        and can_defeat_bokoblins(state, player)
        and (has_practice_sword(state, player) or has_beetle(state, player)),
    )
    set_rule_if_progression(
        "Faron Woods - Rupee on Hollow Tree Root",
        lambda state: can_reach_most_of_faron_woods(state, player),
    )
    set_rule_if_progression(
        "Faron Woods - Rupee on Hollow Tree Branch",
        lambda state: can_reach_most_of_faron_woods(state, player)
        and has_beetle(state, player),
    )
    set_rule_if_progression(
        "Faron Woods - Rupee on Platform near Floria Door",
        lambda state: can_reach_most_of_faron_woods(state, player)
        and has_beetle(state, player),
    )
    set_rule_if_progression(
        "Faron Woods - Deep Woods Chest",
        lambda state: can_reach_deep_woods_after_beehive(state, player),
    )
    set_rule_if_progression(
        "Faron Woods - Chest behind Upper Bombable Rock",
        lambda state: can_reach_most_of_faron_woods(state, player)
        and state.has("Bomb Bag", player),
    )
    set_rule_if_progression(
        "Faron Woods - Chest inside Great Tree",
        lambda state: (
            can_reach_great_tree(state, player) and state.has("Gust Bellows", player)
        )
        or (
            can_reach_top_of_great_tree(state, player)
            and can_defeat_moblins(state, player)
        ),
    )
    set_rule_if_progression(
        "Faron Woods - Rupee on Great Tree North Branch",
        lambda state: can_reach_top_of_great_tree(state, player)
        and has_beetle(state, player),
    )
    set_rule_if_progression(
        "Faron Woods - Rupee on Great Tree West Branch",
        lambda state: can_reach_top_of_great_tree(state, player)
        and has_beetle(state, player),
    )

    # Lake Floria
    set_rule_if_progression(
        "Lake Floria - Rupee under Central Boulder",
        lambda state: can_access_lake_floria(state, player),
    )
    set_rule_if_progression(
        "Lake Floria - Rupee behind Southwest Boulder",
        lambda state: can_access_lake_floria(state, player),
    )
    set_rule_if_progression(
        "Lake Floria - Left Rupee behind Northwest Boulder",
        lambda state: can_access_lake_floria(state, player),
    )
    set_rule_if_progression(
        "Lake Floria - Right Rupee behind Northwest Boulder",
        lambda state: can_access_lake_floria(state, player),
    )
    set_rule_if_progression(
        "Lake Floria - Lake Floria Chest",
        lambda state: can_access_lake_floria(state, player),
    )
    set_rule_if_progression(
        "Lake Floria - Dragon Lair South Chest",
        lambda state: can_reach_floria_waterfall(state, player)
        and state.has("Water Dragon's Scale", player),
    )
    set_rule_if_progression(
        "Lake Floria - Dragon Lair East Chest",
        lambda state: can_reach_floria_waterfall(state, player),
    )
    set_rule_if_progression(
        "Lake Floria - Rupee on High Ledge outside Ancient Cistern Entrance",
        lambda state: can_reach_floria_waterfall(state, player)
        and has_beetle(state, player),
    )

    # Flooded Faron Woods
    set_rule_if_progression(
        "Flooded Faron Woods - Yellow Tadtone under Lilypad",
        lambda state: can_access_flooded_faron_woods(state, player)
        and state.has("Water Dragon's Scale", player),
    )
    set_rule_if_progression(
        "Flooded Faron Woods - 8 Light Blue Tadtones near Viewing Platform",
        lambda state: can_access_flooded_faron_woods(state, player)
        and state.has("Water Dragon's Scale", player),
    )
    set_rule_if_progression(
        "Flooded Faron Woods - 4 Purple Tadtones under Viewing Platform",
        lambda state: can_access_flooded_faron_woods(state, player)
        and state.has("Water Dragon's Scale", player),
    )
    set_rule_if_progression(
        "Flooded Faron Woods - Red Moving Tadtone near Viewing Platform",
        lambda state: can_access_flooded_faron_woods(state, player)
        and state.has("Water Dragon's Scale", player),
    )
    set_rule_if_progression(
        "Flooded Faron Woods - Light Blue Tadtone under Great Tree Root",
        lambda state: can_access_flooded_faron_woods(state, player)
        and state.has("Water Dragon's Scale", player),
    )
    set_rule_if_progression(
        "Flooded Faron Woods - 8 Yellow Tadtones near Kikwi Elder",
        lambda state: can_access_flooded_faron_woods(state, player)
        and state.has("Water Dragon's Scale", player),
    )
    set_rule_if_progression(
        "Flooded Faron Woods - 4 Light Blue Moving Tadtones under Kikwi Elder",
        lambda state: can_access_flooded_faron_woods(state, player)
        and state.has("Water Dragon's Scale", player),
    )
    set_rule_if_progression(
        "Flooded Faron Woods - 4 Red Moving Tadtones North West of Great Tree",
        lambda state: can_access_flooded_faron_woods(state, player)
        and state.has("Water Dragon's Scale", player),
    )
    set_rule_if_progression(
        "Flooded Faron Woods - Green Tadtone behind Upper Bombable Rock",
        lambda state: can_access_flooded_faron_woods(state, player)
        and state.has("Water Dragon's Scale", player),
    )
    set_rule_if_progression(
        "Flooded Faron Woods - 2 Dark Blue Tadtones in Grass West of Great Tree",
        lambda state: can_access_flooded_faron_woods(state, player)
        and state.has("Water Dragon's Scale", player),
    )
    set_rule_if_progression(
        "Flooded Faron Woods - 8 Green Tadtones in West Tunnel",
        lambda state: can_access_flooded_faron_woods(state, player)
        and state.has("Water Dragon's Scale", player),
    )
    set_rule_if_progression(
        "Flooded Faron Woods - 2 Red Tadtones in Grass near Lower Bombable Rock",
        lambda state: can_access_flooded_faron_woods(state, player)
        and state.has("Water Dragon's Scale", player),
    )
    set_rule_if_progression(
        "Flooded Faron Woods - 16 Dark Blue Tadtones in the South West",
        lambda state: can_access_flooded_faron_woods(state, player)
        and state.has("Water Dragon's Scale", player),
    )
    set_rule_if_progression(
        "Flooded Faron Woods - 4 Purple Moving Tadtones near Floria Gate",
        lambda state: can_access_flooded_faron_woods(state, player)
        and state.has("Water Dragon's Scale", player),
    )
    set_rule_if_progression(
        "Flooded Faron Woods - Dark Blue Moving Tadtone inside Small Hollow Tree",
        lambda state: can_access_flooded_faron_woods(state, player)
        and state.has("Water Dragon's Scale", player),
    )
    set_rule_if_progression(
        "Flooded Faron Woods - 4 Yellow Tadtones under Small Hollow Tree",
        lambda state: can_access_flooded_faron_woods(state, player)
        and state.has("Water Dragon's Scale", player),
    )
    set_rule_if_progression(
        "Flooded Faron Woods - 8 Purple Tadtones in Clearing after Small Hollow Tree",
        lambda state: can_access_flooded_faron_woods(state, player)
        and state.has("Water Dragon's Scale", player),
    )
    set_rule_if_progression(
        "Flooded Faron Woods - Water Dragon's Reward",
        lambda state: can_access_flooded_faron_woods(state, player)
        and state.has("Group of Tadtones", player, 17),
    )

    # Eldin Volcano
    set_rule_if_progression(
        "Eldin Volcano - Rupee on Ledge before First Room",
        lambda state: can_access_eldin_volcano(state, player),
    )
    set_rule_if_progression(
        "Eldin Volcano - Chest behind Bombable Wall in First Room",
        lambda state: can_access_eldin_volcano(state, player),
    )
    set_rule_if_progression(
        "Eldin Volcano - Rupee behind Bombable Wall in First Room",
        lambda state: can_access_eldin_volcano(state, player),
    )
    set_rule_if_progression(
        "Eldin Volcano - Rupee in Crawlspace in First Room",
        lambda state: can_access_eldin_volcano(state, player),
    )
    set_rule_if_progression(
        "Eldin Volcano - Chest after Crawlspace",
        lambda state: can_access_eldin_volcano(state, player),
    )
    set_rule_if_progression(
        "Eldin Volcano - Southeast Rupee above Mogma Turf Entrance",
        lambda state: can_access_eldin_volcano(state, player)
        and has_beetle(state, player),
    )
    set_rule_if_progression(
        "Eldin Volcano - North Rupee above Mogma Turf Entrance",
        lambda state: can_access_eldin_volcano(state, player)
        and has_beetle(state, player),
    )
    set_rule_if_progression(
        "Eldin Volcano - Chest behind Bombable Wall near Cliff",
        lambda state: can_access_eldin_volcano(state, player),
    )
    set_rule_if_progression(
        "Eldin Volcano - Item on Cliff",
        lambda state: can_access_eldin_volcano(state, player),
    )
    set_rule_if_progression(
        "Eldin Volcano - Chest behind Bombable Wall near Volcano Ascent",
        lambda state: can_reach_second_part_of_eldin_volcano(state, player),
    )
    set_rule_if_progression(
        "Eldin Volcano - Left Rupee behind Bombable Wall on First Slope",
        lambda state: can_reach_second_part_of_eldin_volcano(state, player),
    )
    set_rule_if_progression(
        "Eldin Volcano - Right Rupee behind Bombable Wall on First Slope",
        lambda state: can_reach_second_part_of_eldin_volcano(state, player),
    )
    set_rule_if_progression(
        "Eldin Volcano - Digging Spot in front of Earth Temple",
        lambda state: can_reach_second_part_of_eldin_volcano(state, player)
        and has_digging_mitts(state, player),
    )
    set_rule_if_progression(
        "Eldin Volcano - Digging Spot below Tower",
        lambda state: can_reach_second_part_of_eldin_volcano(state, player)
        and has_digging_mitts(state, player),
    )
    set_rule_if_progression(
        "Eldin Volcano - Digging Spot behind Boulder on Sandy Slope",
        lambda state: can_reach_second_part_of_eldin_volcano(state, player)
        and has_digging_mitts(state, player),
    )
    set_rule_if_progression(
        "Eldin Volcano - Digging Spot after Vents",
        lambda state: can_reach_second_part_of_eldin_volcano(state, player)
        and has_digging_mitts(state, player)
        and can_survive_eldin_hot_cave(state, player),
    )
    set_rule_if_progression(
        "Eldin Volcano - Digging Spot after Draining Lava",
        lambda state: can_reach_second_part_of_eldin_volcano(state, player)
        and has_digging_mitts(state, player)
        and (
            can_survive_eldin_hot_cave(state, player) or state.has("Bomb Bag", player)
        ),
    )

    # Mogma Turf
    set_rule_if_progression(
        "Mogma Turf - Free Fall Chest",
        lambda state: can_access_mogma_turf(state, player),
    )
    set_rule_if_progression(
        "Mogma Turf - Chest behind Bombable Wall at Entrance",
        lambda state: can_access_mogma_turf(state, player),
    )
    set_rule_if_progression(
        "Mogma Turf - Defeat Bokoblins",
        lambda state: can_access_mogma_turf(state, player)
        and can_defeat_bokoblins(state, player),
    )
    set_rule_if_progression(
        "Mogma Turf - Sand Slide Chest",
        lambda state: can_reach_second_part_of_mogma_turf(state, player),
    )
    set_rule_if_progression(
        "Mogma Turf - Chest behind Bombable Wall in Fire Maze",
        lambda state: can_reach_second_part_of_mogma_turf(state, player),
    )

    # Volcano Summit
    set_rule_if_progression(
        "Volcano Summit - Chest behind Bombable Wall in Waterfall Area",
        lambda state: can_access_volcano_summit(state, player)
        and state.has("Clawshots", player),
    )
    set_rule_if_progression(
        "Volcano Summit - Item behind Digging",
        lambda state: can_pass_volcano_summit_first_frog(state, player)
        and has_mogma_mitts(state, player),
    )

    # Boko Base
    set_rule_if_progression(
        "Bokoblin Base - Plats' Gift",
        lambda state: can_access_bokoblin_base(state, player),
    )
    set_rule_if_progression(
        "Bokoblin Base - Chest near Bone Bridge",
        lambda state: can_access_bokoblin_base(state, player)
        and has_mogma_mitts(state, player),
    )
    set_rule_if_progression(
        "Bokoblin Base - Chest on Cliff",
        lambda state: can_access_bokoblin_base(state, player)
        and has_mogma_mitts(state, player)
        and state.has("Gust Bellows", player),
    )
    set_rule_if_progression(
        "Bokoblin Base - Chest near Drawbridge",
        lambda state: can_access_bokoblin_base(state, player)
        and has_mogma_mitts(state, player)
        and (
            state.has("Clawshots", player)
            or can_bypass_boko_base_watchtower(state, player)
        ),
    )
    set_rule_if_progression(
        "Bokoblin Base - Chest East of Earth Temple Entrance",
        lambda state: can_access_bokoblin_base(state, player)
        and has_mogma_mitts(state, player)
        and state.has("Clawshots", player)
        and (
            state.has("Bomb Bag", player)
            or (
                can_bypass_boko_base_watchtower(state, player)
                and state.has("Whip", player)
            )
        ),
    )
    set_rule_if_progression(
        "Bokoblin Base - Chest West of Earth Temple Entrance",
        lambda state: can_access_bokoblin_base(state, player)
        and has_mogma_mitts(state, player)
        and state.has("Clawshots", player)
        and (
            state.has("Bomb Bag", player)
            or (
                can_bypass_boko_base_watchtower(state, player)
                and state.has("Whip", player)
            )
        ),
    )
    set_rule_if_progression(
        "Bokoblin Base - First Chest in Volcano Summit",
        lambda state: can_access_bokoblin_base(state, player)
        and has_mogma_mitts(state, player)
        and state.has("Clawshots", player)
        and state.has("Bomb Bag", player)
        and state.has("Fireshield Earrings", player),
    )
    set_rule_if_progression(
        "Bokoblin Base - Raised Chest in Volcano Summit",
        lambda state: can_access_bokoblin_base(state, player)
        and has_mogma_mitts(state, player)
        and state.has("Clawshots", player)
        and state.has("Bomb Bag", player)
        and state.has("Fireshield Earrings", player),
    )
    set_rule_if_progression(
        "Bokoblin Base - Chest in Volcano Summit Alcove",
        lambda state: can_access_bokoblin_base(state, player)
        and has_mogma_mitts(state, player)
        and state.has("Clawshots", player)
        and state.has("Bomb Bag", player)
        and state.has("Fireshield Earrings", player)
        and has_practice_sword(state, player),
    )
    set_rule_if_progression(
        "Bokoblin Base - Fire Dragon's Reward",
        lambda state: can_access_bokoblin_base(state, player)
        and has_mogma_mitts(state, player)
        and state.has("Clawshots", player)
        and state.has("Bomb Bag", player)
        and state.has("Fireshield Earrings", player)
        and (has_beetle(state, player) or has_bow(state, player)),
    )

    # Lanayru Mine
    set_rule_if_progression(
        "Lanayru Mine - Chest behind First Landing",
        lambda state: can_access_lanayru_mine(state, player)
        and state.has("Clawshots", player),
    )
    set_rule_if_progression(
        "Lanayru Mine - Chest near First Timeshift Stone",
        lambda state: can_access_lanayru_mine(state, player)
        and can_hit_timeshift_stone(state, player),
    )
    set_rule_if_progression(
        "Lanayru Mine - Chest behind Statue",
        lambda state: can_reach_second_part_of_lanayru_mine(state, player)
        and (state.has("Bomb Bag", player) or has_hook_beetle(state, player)),
    )
    set_rule_if_progression(
        "Lanayru Mine - Chest at the End of Mine",
        lambda state: can_reach_second_part_of_lanayru_mine(state, player),
    )

    # Lanayru Desert
    set_rule_if_progression(
        "Lanayru Desert - Chest near Party Wheel",
        lambda state: can_access_lanayru_desert(state, player)
        and state.has("Bomb Bag", player),
    )
    set_rule_if_progression(
        "Lanayru Desert - Chest near Caged Robot",
        lambda state: can_access_lanayru_desert(state, player),
    )
    set_rule_if_progression(
        "Lanayru Desert - Rescue Caged Robot",
        lambda state: can_access_lanayru_desert(state, player)
        and (state.has("Bomb Bag", player) or has_hook_beetle(state, player)),
    )
    set_rule_if_progression(
        "Lanayru Desert - Chest on Platform near Fire Node",
        lambda state: can_reach_second_part_of_lanayru_desert(state, player)
        and state.has("Clawshots", player),
    )
    set_rule_if_progression(
        "Lanayru Desert - Chest on Platform near Lightning Node",
        lambda state: can_reach_second_part_of_lanayru_desert(state, player)
        and state.has("Clawshots", player),
    )
    set_rule_if_progression(
        "Lanayru Desert - Chest near Sand Oasis",
        lambda state: can_access_lanayru_desert(state, player)
        and state.has("Clawshots", player),
    )
    set_rule_if_progression(
        "Lanayru Desert - Chest on top of Lanayru Mining Facility",
        lambda state: can_raise_lmf(state, player),
    )
    set_rule_if_progression(
        "Lanayru Desert - Secret Passageway Chest",
        lambda state: can_reach_second_part_of_lanayru_desert(state, player)
        and (state.has("Bomb Bag", player) or has_tough_beetle(state, player)),
    )

    # Fire node
    set_rule_if_progression(
        "Lanayru Desert - Shortcut Chest",
        lambda state: can_reach_second_part_of_lanayru_desert(state, player)
        and can_defeat_ampilus(state, player),
    )
    set_rule_if_progression(
        "Lanayru Desert - First Small Chest",
        lambda state: can_reach_second_part_of_lanayru_desert(state, player)
        and state.has("Bomb Bag", player),
    )
    set_rule_if_progression(
        "Lanayru Desert - Second Small Chest",
        lambda state: can_reach_second_part_of_lanayru_desert(state, player)
        and state.has("Bomb Bag", player),
    )
    set_rule_if_progression(
        "Lanayru Desert - Left Ending Chest",
        lambda state: can_reach_second_part_of_lanayru_desert(state, player)
        and can_defeat_ampilus(state, player)
        and state.has("Bomb Bag", player)
        and has_hook_beetle(state, player),
    )
    set_rule_if_progression(
        "Lanayru Desert - Right Ending Chest",
        lambda state: can_reach_second_part_of_lanayru_desert(state, player)
        and can_defeat_ampilus(state, player)
        and state.has("Bomb Bag", player)
        and has_hook_beetle(state, player),
    )

    # Lightning node
    set_rule_if_progression(
        "Lanayru Desert - First Chest",
        lambda state: can_reach_second_part_of_lanayru_desert(state, player)
        and state.has("Bomb Bag", player),
    )
    set_rule_if_progression(
        "Lanayru Desert - Second Chest",
        lambda state: can_reach_second_part_of_lanayru_desert(state, player)
        and state.has("Bomb Bag", player),
    )
    set_rule_if_progression(
        "Lanayru Desert - Raised Chest near Generator",
        lambda state: can_reach_second_part_of_lanayru_desert(state, player)
        and state.has("Bomb Bag", player)
        and (has_beetle(state, player) or has_bow(state, player)),
    )

    # Lanayru Caves
    set_rule_if_progression(
        "Lanayru Caves - Chest", lambda state: can_access_lanayru_caves(state, player)
    )
    set_rule_if_progression(
        "Lanayru Caves - Golo's Gift",  # Clawshots needed to for Golo to spawn
        lambda state: can_access_lanayru_caves(state, player)
        and state.has("Clawshots", player),
    )

    # Lanayru Gorge
    set_rule_if_progression(
        "Lanayru Gorge - Thunder Dragon's Reward",
        lambda state: can_access_lanayru_gorge(state, player)
        and can_hit_timeshift_stone(state, player)
        and state.has("Life Tree Fruit", player),
    )
    set_rule_if_progression(
        "Lanayru Gorge - Item on Pillar",
        lambda state: can_access_lanayru_gorge(state, player)
        and has_beetle(state, player),
    )
    set_rule_if_progression(
        "Lanayru Gorge - Digging Spot",
        lambda state: can_access_lanayru_gorge(state, player)
        and can_hit_timeshift_stone(state, player)
        and state.has("Gust Bellows", player)
        and has_digging_mitts(state, player),
    )

    # Lanayru Sand Sea
    set_rule_if_progression(
        "Lanayru Sand Sea - Ancient Harbour - Rupee on First Pillar",
        lambda state: can_access_lanayru_sand_sea(state, player)
        and has_beetle(state, player),
    )
    set_rule_if_progression(
        "Lanayru Sand Sea - Ancient Harbour - Left Rupee on Entrance Crown",
        lambda state: can_access_lanayru_sand_sea(state, player)
        and has_quick_beetle(state, player),
    )
    set_rule_if_progression(
        "Lanayru Sand Sea - Ancient Harbour - Right Rupee on Entrance Crown",
        lambda state: can_access_lanayru_sand_sea(state, player)
        and has_quick_beetle(state, player),
    )
    set_rule_if_progression(
        "Lanayru Sand Sea - Skipper's Retreat - Chest after Moblin",
        lambda state: can_access_lanayru_sand_sea(state, player)
        and (state.has("Bomb Bag", player) or has_hook_beetle(state, player)),
    )
    set_rule_if_progression(
        "Lanayru Sand Sea - Skipper's Retreat - Chest on top of Cacti Pillar",
        lambda state: can_access_lanayru_sand_sea(state, player)
        and state.has("Whip", player)
        and state.has("Clawshots", player)
        and (state.has("Bomb Bag", player) or has_hook_beetle(state, player))
        and (
            has_slingshot(state, player)
            or has_beetle(state, player)
            or has_bow(state, player)
        ),
    )
    set_rule_if_progression(
        "Lanayru Sand Sea - Skipper's Retreat - Chest in Shack",
        lambda state: can_access_lanayru_sand_sea(state, player)
        and state.has("Whip", player)
        and state.has("Clawshots", player)
        and (state.has("Bomb Bag", player) or has_hook_beetle(state, player))
        and (
            has_slingshot(state, player)
            or has_beetle(state, player)
            or has_bow(state, player)
        )
        and state.has("Gust Bellows", player),
    )
    set_rule_if_progression(
        "Lanayru Sand Sea - Skipper's Retreat - Skydive Chest",
        lambda state: can_access_lanayru_sand_sea(state, player)
        and state.has("Whip", player)
        and state.has("Clawshots", player)
        and (state.has("Bomb Bag", player) or has_hook_beetle(state, player))
        and (
            has_slingshot(state, player)
            or has_beetle(state, player)
            or has_bow(state, player)
        ),
    )
    set_rule_if_progression(
        "Lanayru Sand Sea - Rickety Coaster -- Heart Stopping Track in 1'05",
        lambda state: can_access_lanayru_sand_sea(state, player)
        and state.has("Gust Bellows", player)
        and can_defeat_moldarachs(state, player),
    )
    set_rule_if_progression(
        "Lanayru Sand Sea - Pirate Stronghold - Rupee on East Sea Pillar",
        lambda state: can_access_lanayru_sand_sea(state, player)
        and has_quick_beetle(state, player),
    )
    set_rule_if_progression(
        "Lanayru Sand Sea - Pirate Stronghold - Rupee on West Sea Pillar",
        lambda state: can_access_lanayru_sand_sea(state, player)
        and has_quick_beetle(state, player),
    )
    set_rule_if_progression(
        "Lanayru Sand Sea - Pirate Stronghold - Rupee on Bird Statue Pillar or Nose",
        lambda state: can_access_lanayru_sand_sea(state, player)
        and has_beetle(state, player),
    )
    set_rule_if_progression(
        "Lanayru Sand Sea - Pirate Stronghold - First Chest",
        lambda state: can_access_lanayru_sand_sea(state, player),
    )
    set_rule_if_progression(
        "Lanayru Sand Sea - Pirate Stronghold - Second Chest",
        lambda state: can_access_lanayru_sand_sea(state, player),
    )
    set_rule_if_progression(
        "Lanayru Sand Sea - Pirate Stronghold - Third Chest",
        lambda state: can_access_lanayru_sand_sea(state, player),
    )

    # Skyview
    set_rule_if_progression(
        "Skyview - Chest on Tree Branch",
        lambda state: can_reach_SV_second_room(state, player)
        and (
            distance_activator(state, player)
            or has_goddess_sword(state, player)
            or state.has("Whip", player)
        ),
    )
    set_rule_if_progression(
        "Skyview - Digging Spot in Crawlspace",
        lambda state: can_reach_SV_second_room(state, player)
        and distance_activator(state, player)
        and state.has("Water Dragon's Scale", player)
        and has_digging_mitts(state, player),
    )
    set_rule_if_progression(
        "Skyview - Chest behind Two Eyes",
        lambda state: can_reach_SV_second_room(state, player)
        and (state.has("Clawshots", player) or distance_activator(state, player))
        and has_practice_sword(state, player),
    )
    set_rule_if_progression(
        "Skyview - Chest after Stalfos Fight",
        lambda state: can_reach_SV_main_room(state, player)
        and distance_activator(
            state, player
        )  # Sword for fight, or scale to skip fight in SV 2
        and (
            has_practice_sword(state, player)
            or state.has("Water Dragon's Scale", player)
        ),
    )
    set_rule_if_progression(
        "Skyview - Item behind Bars",
        lambda state: can_reach_SV_main_room(state, player)
        and (
            has_beetle(state, player) or state.has("Whip", player)
        ),  # Beetle for crystal or whip item
    )
    set_rule_if_progression(
        "Skyview - Rupee in Southeast Tunnel",
        lambda state: can_reach_SV_main_room(state, player)
        and has_beetle(state, player),
    )
    set_rule_if_progression(
        "Skyview - Rupee in Southwest Tunnel",
        lambda state: can_reach_SV_main_room(state, player)
        and has_beetle(state, player),
    )
    set_rule_if_progression(
        "Skyview - Rupee in East Tunnel",
        lambda state: can_reach_SV_main_room(state, player)
        and has_beetle(state, player),
    )
    set_rule_if_progression(
        "Skyview - Chest behind Three Eyes",
        lambda state: can_reach_SV_main_room(state, player)
        and has_beetle(state, player)
        and has_practice_sword(state, player),
    )
    set_rule_if_progression(
        "Skyview - Chest near Boss Door",
        lambda state: can_reach_SV_boss_door(state, player),
    )
    set_rule_if_progression(
        "Skyview - Boss Key Chest",
        lambda state: can_reach_SV_boss_door(state, player)
        and (
            upgraded_skyward_strike(state, player) or distance_activator(state, player)
        ),  # to hit vines
    )
    set_rule_if_progression(
        "Skyview - Heart Container", lambda state: can_beat_ghirahim_1(state, player)
    )
    set_rule_if_progression(
        "Skyview - Rupee on Spring Pillar",
        lambda state: can_beat_ghirahim_1(state, player) and has_beetle(state, player),
    )
    set_rule_if_progression(
        "Skyview - Strike Crest", lambda state: can_beat_SV(state, player)
    )

    # Earth Temple
    set_rule_if_progression(
        "Earth Temple - Vent Chest",
        lambda state: state.can_reach_region("Earth Temple", player)
        and has_digging_mitts(state, player),
    )
    set_rule_if_progression(
        "Earth Temple - Rupee above Drawbridge",
        lambda state: state.can_reach_region("Earth Temple", player)
        and has_beetle(state, player),
    )
    set_rule_if_progression(
        "Earth Temple - Chest behind Bombable Rock",
        lambda state: can_reach_ET_main_room(state, player),
    )
    set_rule_if_progression(
        "Earth Temple - Chest Left of Main Room Bridge",
        lambda state: can_reach_ET_main_room(state, player),
    )
    set_rule_if_progression(
        "Earth Temple - Chest in West Room",
        lambda state: can_reach_ET_main_room(state, player)
        and (state.has("Bomb Bag", player) or has_hook_beetle(state, player)),
    )
    set_rule_if_progression(
        "Earth Temple - Chest after Double Lizalfos Fight",
        lambda state: can_reach_ET_main_room(state, player)
        and can_defeat_lezalfos(state, player),
    )
    set_rule_if_progression(
        "Earth Temple - Ledd's Gift",
        lambda state: can_reach_ET_main_room(state, player)
        and can_defeat_lezalfos(state, player),
    )
    set_rule_if_progression(
        "Earth Temple - Rupee in Lava Tunnel",
        lambda state: can_pass_ET_boulder_section(state, player),
    )
    set_rule_if_progression(
        "Earth Temple - Chest Guarded by Lizalfos",
        lambda state: can_pass_ET_boulder_section(state, player),
    )
    set_rule_if_progression(
        "Earth Temple - Boss Key Chest",
        lambda state: can_reach_ET_boss_door(state, player),
    )
    set_rule_if_progression(
        "Earth Temple - Heart Container", lambda state: can_beat_scaldera(state, player)
    )
    set_rule_if_progression(
        "Earth Temple - Strike Crest", lambda state: can_beat_ET(state, player)
    )

    # Lanayru Mining Facility
    set_rule_if_progression(
        "Lanayru Mining Facility - Chest behind Bars",
        lambda state: state.can_reach_region("Lanayru Mining Facility", player),
    )
    set_rule_if_progression(
        "Lanayru Mining Facility - First Chest in Hub Room",
        lambda state: can_reach_LMF_hub_room(state, player),
    )
    set_rule_if_progression(
        "Lanayru Mining Facility - Chest in First West Room",
        lambda state: can_reach_LMF_second_room(state, player)
        and state.has("Gust Bellows", player),
    )
    set_rule_if_progression(
        "Lanayru Mining Facility - Chest after Armos Fight",
        lambda state: can_reach_LMF_hub_room_west(state, player),
    )
    set_rule_if_progression(
        "Lanayru Mining Facility - Chest in Key Locked Room",
        lambda state: can_reach_LMF_key_locked_room_in_past(state, player),
    )
    set_rule_if_progression(
        "Lanayru Mining Facility - Raised Chest in Hop across Boxes Room",
        lambda state: can_reach_LMF_key_locked_room_in_past(state, player)
        and (
            distance_activator(state, player)
            or has_practice_sword(state, player)
            or state.has("Gust Bellows", player)
            or state.has("Whip", player)
            or state.has("Bomb Bag", player)
        ),
    )
    set_rule_if_progression(
        "Lanayru Mining Facility - Lower Chest in Hop across Boxes Room",
        lambda state: can_reach_LMF_key_locked_room_in_past(state, player)
        and (
            distance_activator(state, player)
            or has_practice_sword(state, player)
            or state.has("Gust Bellows", player)
            or state.has("Whip", player)
            or state.has("Bomb Bag", player)
        ),
    )
    set_rule_if_progression(
        "Lanayru Mining Facility - Chest behind First Crawlspace",
        lambda state: can_reach_LMF_hub_room_west(state, player)
        and state.has("Gust Bellows", player),
    )
    set_rule_if_progression(
        "Lanayru Mining Facility - Chest in Spike Maze",
        lambda state: can_reach_LMF_hub_room_west(state, player)
        and state.has("Gust Bellows", player),
    )
    set_rule_if_progression(
        "Lanayru Mining Facility - Boss Key Chest",
        lambda state: can_pass_LMF_boss_key_room(state, player),
    )
    set_rule_if_progression(
        "Lanayru Mining Facility - Shortcut Chest in Main Hub",
        lambda state: can_pass_LMF_boss_key_room(state, player),
    )
    set_rule_if_progression(
        "Lanayru Mining Facility - Heart Container",
        lambda state: can_beat_moldarach(state, player),
    )
    set_rule_if_progression(
        "Lanayru Mining Facility - Exit Hall of Ancient Robots",
        lambda state: can_beat_LMF(state, player),
    )

    # Ancient Cistern
    set_rule_if_progression(
        "Ancient Cistern - Rupee in West Hand",
        lambda state: state.can_reach_region("Ancient Cistern", player)
        and state.has("Water Dragon's Scale", player),
    )
    set_rule_if_progression(
        "Ancient Cistern - Rupee in East Hand",
        lambda state: state.can_reach_region("Ancient Cistern", player)
        and state.has("Water Dragon's Scale", player),
    )
    set_rule_if_progression(
        "Ancient Cistern - First Rupee in East Part in Short Tunnel",
        lambda state: state.can_reach_region("Ancient Cistern", player)
        and state.has("Water Dragon's Scale", player)
        and can_unlock_combination_lock(state, player),
    )
    set_rule_if_progression(
        "Ancient Cistern - Second Rupee in East Part in Short Tunnel",
        lambda state: state.can_reach_region("Ancient Cistern", player)
        and state.has("Water Dragon's Scale", player)
        and can_unlock_combination_lock(state, player),
    )
    set_rule_if_progression(
        "Ancient Cistern - Third Rupee in East Part in Short Tunnel",
        lambda state: state.can_reach_region("Ancient Cistern", player)
        and state.has("Water Dragon's Scale", player)
        and can_unlock_combination_lock(state, player),
    )
    set_rule_if_progression(
        "Ancient Cistern - Rupee in East Part in Cubby",
        lambda state: state.can_reach_region("Ancient Cistern", player)
        and state.has("Water Dragon's Scale", player)
        and can_unlock_combination_lock(state, player),
    )
    set_rule_if_progression(
        "Ancient Cistern - Rupee in East Part in Main Tunnel",
        lambda state: state.can_reach_region("Ancient Cistern", player)
        and state.has("Water Dragon's Scale", player)
        and can_unlock_combination_lock(state, player),
    )
    set_rule_if_progression(
        "Ancient Cistern - Chest in East Part",
        lambda state: state.can_reach_region("Ancient Cistern", player)
        and state.has("Water Dragon's Scale", player)
        and can_unlock_combination_lock(state, player),
    )
    set_rule_if_progression(
        "Ancient Cistern - Chest after Whip Hooks",
        lambda state: state.can_reach_region("Ancient Cistern", player)
        and state.has("Whip", player),
    )
    set_rule_if_progression(
        "Ancient Cistern - Chest near Vines",
        lambda state: can_reach_AC_vines(state, player),
    )
    set_rule_if_progression(
        "Ancient Cistern - Chest behind the Waterfall",
        lambda state: can_pass_AC_waterfall(state, player),
    )
    set_rule_if_progression(
        "Ancient Cistern - Bokoblin",
        lambda state: can_reach_AC_boko_key_door(state, player)
        and state.has("Whip", player),
    )
    set_rule_if_progression(
        "Ancient Cistern - Rupee under Lilypad",
        lambda state: can_reach_AC_boko_key_door(state, player)
        and state.has("Ancient Cistern Small Key", player, 2)
        and state.has("Water Dragon's Scale", player)
        and state.has("Whip", player),
    )
    set_rule_if_progression(
        "Ancient Cistern - Chest in Key Locked Room",
        lambda state: can_enter_AC_statue(state, player)
        and state.has("Ancient Cistern Small Key", player, 2)
        and (
            can_defeat_stalmaster(state, player) or can_lower_AC_statue(state, player)
        ),
    )
    set_rule_if_progression(
        "Ancient Cistern - Boss Key Chest",
        lambda state: can_reach_AC_thread(state, player) and state.has("Whip", player),
    )
    set_rule_if_progression(
        "Ancient Cistern - Heart Container",
        lambda state: can_beat_koloktos(state, player),
    )
    set_rule_if_progression(
        "Ancient Cistern - Farore's Flame", lambda state: can_beat_AC(state, player)
    )

    # Sandship
    set_rule_if_progression(
        "Sandship - Chest at the Stern",
        lambda state: can_change_SSH_temporality(state, player)
        and has_bow(state, player)
        and state.has("Clawshots", player),
    )
    set_rule_if_progression(
        "Sandship - Chest before 4-Door Corridor",
        lambda state: can_change_SSH_temporality(state, player)
        and has_bow(state, player),
    )
    set_rule_if_progression(
        "Sandship - Chest behind Combination Lock",
        lambda state: can_unlock_combination_lock(state, player)
        and (
            (
                can_reach_SSH_4_door_corridor(state, player)
                and state.has("Gust Bellows", player)
            )
            or can_change_SSH_temporality(state, player)
        ),
    )
    set_rule_if_progression(
        "Sandship - Treasure Room First Chest",
        lambda state: can_reach_SSH_brig(state, player),
    )
    set_rule_if_progression(
        "Sandship - Treasure Room Second Chest",
        lambda state: can_reach_SSH_brig(state, player),
    )
    set_rule_if_progression(
        "Sandship - Treasure Room Third Chest",
        lambda state: can_reach_SSH_brig(state, player),
    )
    set_rule_if_progression(
        "Sandship - Treasure Room Fourth Chest",
        lambda state: can_reach_SSH_brig(state, player),
    )
    set_rule_if_progression(
        "Sandship - Treasure Room Fifth Chest",
        lambda state: can_reach_SSH_brig(state, player),
    )
    set_rule_if_progression(
        "Sandship - Robot in Brig's Reward",
        lambda state: can_reach_SSH_brig(state, player),
    )
    set_rule_if_progression(
        "Sandship - Chest after Scervo Fight",
        lambda state: state.can_reach_region("Sandship", player)
        and has_practice_sword(state, player)
        and state.has("Sandship Small Key", player, 2),
    )
    set_rule_if_progression(
        "Sandship - Boss Key Chest",
        lambda state: can_change_SSH_temporality(state, player)
        and has_bow(state, player)
        and state.has("Sandship Small Key", player, 2),
    )
    set_rule_if_progression(
        "Sandship - Heart Container", lambda state: can_beat_tentalus(state, player)
    )
    set_rule_if_progression(
        "Sandship - Nayru's Flame", lambda state: can_beat_SSH(state, player)
    )

    # Fire Sanctuary
    set_rule_if_progression(
        "Fire Sanctuary - Chest in First Room",
        lambda state: state.can_reach_region("Fire Sanctuary", player)
        and distance_activator(state, player)
        and can_defeat_bokoblins(state, player),
    )
    set_rule_if_progression(
        "Fire Sanctuary - Chest in Second Room",
        lambda state: can_reach_FS_first_magmanos_room(state, player),
    )
    set_rule_if_progression(
        "Fire Sanctuary - Chest on Balcony",
        lambda state: can_reach_FS_first_magmanos_room(state, player)
        and has_mogma_mitts(state, player)
        and has_practice_sword(state, player),
    )
    set_rule_if_progression(
        "Fire Sanctuary - Chest near First Trapped Mogma",
        lambda state: can_reach_FS_first_magmanos_room(state, player)
        and can_defeat_lezalfos(state, player)
        and has_hook_beetle(state, player)
        and (state.has("Clawshots", player) or state.has("Gust Bellows", player)),
    )
    set_rule_if_progression(
        "Fire Sanctuary - First Chest in Water Fruit Room",
        lambda state: can_reach_FS_water_pod_room(state, player),
    )
    set_rule_if_progression(
        "Fire Sanctuary - Second Chest in Water Fruit Room",
        lambda state: can_reach_FS_water_pod_room(state, player),
    )
    set_rule_if_progression(
        "Fire Sanctuary - Rescue First Trapped Mogma",
        lambda state: can_reach_FS_water_pod_room(state, player)
        and has_practice_sword(state, player),
    )
    set_rule_if_progression(
        "Fire Sanctuary - Rescue Second Trapped Mogma",
        lambda state: can_reach_FS_second_bridge(state, player)
        and state.has("Clawshots", player)
        and has_mogma_mitts(state, player)
        and has_practice_sword(state, player),
    )
    set_rule_if_progression(
        "Fire Sanctuary - Chest after Bombable Wall",
        lambda state: can_reach_FS_second_bridge(state, player)
        and state.has("Clawshots", player)
        and has_mogma_mitts(state, player)
        and has_practice_sword(state, player)
        and state.has("Bomb Bag", player),
    )
    set_rule_if_progression(
        "Fire Sanctuary - Plats' Chest",
        lambda state: can_reach_FS_plats_room(state, player)
        and has_mogma_mitts(state, player),
    )
    set_rule_if_progression(
        "Fire Sanctuary - Chest in Staircase Room",
        lambda state: can_reach_top_of_FS_staircase(state, player),
    )
    set_rule_if_progression(
        "Fire Sanctuary - Boss Key Chest",
        lambda state: can_reach_top_of_FS_staircase(state, player)
        and has_mogma_mitts(state, player),
    )
    set_rule_if_progression(
        "Fire Sanctuary - Heart Container",
        lambda state: can_beat_ghirahim_2(state, player),
    )
    set_rule_if_progression(
        "Fire Sanctuary - Din's Flame", lambda state: can_beat_FS(state, player)
    )

    # Sky Keep
    set_rule_if_progression(
        "Sky Keep - First Chest",
        lambda state: state.can_reach_region("Sky Keep", player),
    )
    set_rule_if_progression(
        "Sky Keep - Chest after Dreadfuse",
        lambda state: can_pass_SK_mini_boss_room(state, player),
    )
    set_rule_if_progression(
        "Sky Keep - Rupee in Fire Sanctuary Room in Alcove",
        lambda state: can_pass_SK_fs_room(state, player) and has_beetle(state, player),
    )
    set_rule_if_progression(
        "Sky Keep - Sacred Power of Din",
        lambda state: can_get_triforce_of_power(state, player),
    )
    set_rule_if_progression(
        "Sky Keep - Sacred Power of Nayru",
        lambda state: can_get_triforce_of_wisdom(state, player),
    )
    set_rule_if_progression(
        "Sky Keep - Sacred Power of Farore",
        lambda state: can_get_triforce_of_courage(state, player),
    )

    # Silent Realms
    ## Trial Rewards
    set_rule_if_progression(
        "Skyloft Silent Realm - Trial Reward",
        lambda state: can_access_skyloft_silent_realm(state, player),
    )
    set_rule_if_progression(
        "Faron Silent Realm - Trial Reward",
        lambda state: can_access_faron_silent_realm(state, player),
    )
    set_rule_if_progression(
        "Eldin Silent Realm - Trial Reward",
        lambda state: can_access_eldin_silent_realm(state, player),
    )
    set_rule_if_progression(
        "Lanayru Silent Realm - Trial Reward",
        lambda state: can_access_lanayru_silent_realm(state, player),
    )

    ## Skyloft Relics
    set_rule_if_progression(
        "Skyloft Silent Realm - Relic 1",
        lambda state: can_access_skyloft_silent_realm(state, player),
    )
    set_rule_if_progression(
        "Skyloft Silent Realm - Relic 2",
        lambda state: can_access_skyloft_silent_realm(state, player),
    )
    set_rule_if_progression(
        "Skyloft Silent Realm - Relic 3",
        lambda state: can_access_skyloft_silent_realm(state, player),
    )
    set_rule_if_progression(
        "Skyloft Silent Realm - Relic 4",
        lambda state: can_access_skyloft_silent_realm(state, player),
    )
    set_rule_if_progression(
        "Skyloft Silent Realm - Relic 5",
        lambda state: can_access_skyloft_silent_realm(state, player),
    )
    set_rule_if_progression(
        "Skyloft Silent Realm - Relic 6",
        lambda state: can_access_skyloft_silent_realm(state, player),
    )
    set_rule_if_progression(
        "Skyloft Silent Realm - Relic 7",
        lambda state: can_access_skyloft_silent_realm(state, player),
    )
    set_rule_if_progression(
        "Skyloft Silent Realm - Relic 8",
        lambda state: can_access_skyloft_silent_realm(state, player),
    )
    set_rule_if_progression(
        "Skyloft Silent Realm - Relic 9",
        lambda state: can_access_skyloft_silent_realm(state, player),
    )
    set_rule_if_progression(
        "Skyloft Silent Realm - Relic 10",
        lambda state: can_access_skyloft_silent_realm(state, player),
    )

    ## Faron Relics
    set_rule_if_progression(
        "Faron Silent Realm - Relic 1",
        lambda state: can_access_faron_silent_realm(state, player),
    )
    set_rule_if_progression(
        "Faron Silent Realm - Relic 2",
        lambda state: can_access_faron_silent_realm(state, player),
    )
    set_rule_if_progression(
        "Faron Silent Realm - Relic 3",
        lambda state: can_access_faron_silent_realm(state, player),
    )
    set_rule_if_progression(
        "Faron Silent Realm - Relic 4",
        lambda state: can_access_faron_silent_realm(state, player),
    )
    set_rule_if_progression(
        "Faron Silent Realm - Relic 5",
        lambda state: can_access_faron_silent_realm(state, player),
    )
    set_rule_if_progression(
        "Faron Silent Realm - Relic 6",
        lambda state: can_access_faron_silent_realm(state, player),
    )
    set_rule_if_progression(
        "Faron Silent Realm - Relic 7",
        lambda state: can_access_faron_silent_realm(state, player),
    )
    set_rule_if_progression(
        "Faron Silent Realm - Relic 8",
        lambda state: can_access_faron_silent_realm(state, player),
    )
    set_rule_if_progression(
        "Faron Silent Realm - Relic 9",
        lambda state: can_access_faron_silent_realm(state, player),
    )
    set_rule_if_progression(
        "Faron Silent Realm - Relic 10",
        lambda state: can_access_faron_silent_realm(state, player),
    )

    ## Eldin Relics
    set_rule_if_progression(
        "Eldin Silent Realm - Relic 1",
        lambda state: can_access_eldin_silent_realm(state, player),
    )
    set_rule_if_progression(
        "Eldin Silent Realm - Relic 2",
        lambda state: can_access_eldin_silent_realm(state, player),
    )
    set_rule_if_progression(
        "Eldin Silent Realm - Relic 3",
        lambda state: can_access_eldin_silent_realm(state, player),
    )
    set_rule_if_progression(
        "Eldin Silent Realm - Relic 4",
        lambda state: can_access_eldin_silent_realm(state, player),
    )
    set_rule_if_progression(
        "Eldin Silent Realm - Relic 5",
        lambda state: can_access_eldin_silent_realm(state, player),
    )
    set_rule_if_progression(
        "Eldin Silent Realm - Relic 6",
        lambda state: can_access_eldin_silent_realm(state, player),
    )
    set_rule_if_progression(
        "Eldin Silent Realm - Relic 7",
        lambda state: can_access_eldin_silent_realm(state, player),
    )
    set_rule_if_progression(
        "Eldin Silent Realm - Relic 8",
        lambda state: can_access_eldin_silent_realm(state, player),
    )
    set_rule_if_progression(
        "Eldin Silent Realm - Relic 9",
        lambda state: can_access_eldin_silent_realm(state, player),
    )
    set_rule_if_progression(
        "Eldin Silent Realm - Relic 10",
        lambda state: can_access_eldin_silent_realm(state, player),
    )

    ## Lanayru Relics
    set_rule_if_progression(
        "Lanayru Silent Realm - Relic 1",
        lambda state: can_access_lanayru_silent_realm(state, player),
    )
    set_rule_if_progression(
        "Lanayru Silent Realm - Relic 2",
        lambda state: can_access_lanayru_silent_realm(state, player),
    )
    set_rule_if_progression(
        "Lanayru Silent Realm - Relic 3",
        lambda state: can_access_lanayru_silent_realm(state, player),
    )
    set_rule_if_progression(
        "Lanayru Silent Realm - Relic 4",
        lambda state: can_access_lanayru_silent_realm(state, player),
    )
    set_rule_if_progression(
        "Lanayru Silent Realm - Relic 5",
        lambda state: can_access_lanayru_silent_realm(state, player),
    )
    set_rule_if_progression(
        "Lanayru Silent Realm - Relic 6",
        lambda state: can_access_lanayru_silent_realm(state, player),
    )
    set_rule_if_progression(
        "Lanayru Silent Realm - Relic 7",
        lambda state: can_access_lanayru_silent_realm(state, player),
    )
    set_rule_if_progression(
        "Lanayru Silent Realm - Relic 8",
        lambda state: can_access_lanayru_silent_realm(state, player),
    )
    set_rule_if_progression(
        "Lanayru Silent Realm - Relic 9",
        lambda state: can_access_lanayru_silent_realm(state, player),
    )
    set_rule_if_progression(
        "Lanayru Silent Realm - Relic 10",
        lambda state: can_access_lanayru_silent_realm(state, player),
    )

    set_rule_if_progression(
        "Hylia's Realm - Defeat Demise",
        lambda state: can_reach_and_defeat_demise(state, player),
    )
