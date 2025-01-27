from typing import TYPE_CHECKING

from BaseClasses import ItemClassification as IC
from Fill import FillError

from ..Items import ITEM_TABLE, CONSUMABLE_ITEMS
from ..Locations import LOCATION_TABLE, SSLocType
from ..Constants import *

if TYPE_CHECKING:
    from .. import SSWorld


def handle_itempool(world: "SSWorld") -> None:
    """
    Handles the item pool for the world.

    :param world: The SS game world.
    """

    # Create the itempool.
    pool, precollected_items = _create_itempool(world)

    # Add starting items to the multiworld's `precollected_items` list.
    for item in precollected_items:
        world.multiworld.push_precollected(world.create_item(item))

    placed = _handle_placements(world, pool)
    for itm in placed:
        pool.remove(itm)

    # Create the pool of the remaining shuffled items.
    items = [world.create_item(itm) for itm in pool]
    world.multiworld.random.shuffle(items)

    world.multiworld.itempool += items


def _create_itempool(world: "SSWorld") -> tuple[list[str], list[str]]:
    """
    Creates and fills the item pool and determines starting items.

    :param world: The SS game world.
    :return: A tuple of the item pool and starting items.
    """
    pool: list[str] = []
    starting_items: list[str] = []
    eud = bool(world.options.empty_unrequired_dungeons)

    # Split items into three different pools: progression, useful, and filler.
    progression_pool: list[str] = []
    useful_pool: list[str] = []
    filler_pool: list[str] = []
    for item, data in ITEM_TABLE.items():
        if data.type == "Item":
            adjusted_classification = item_classification(world, item)
            classification = data.classification if adjusted_classification is None else adjusted_classification

            if classification & IC.progression:
                progression_pool.extend([item] * data.quantity)
            elif classification & IC.useful:
                useful_pool.extend([item] * data.quantity)
            else:
                filler_pool.extend([item] * data.quantity)

        # Handle dungeon items
        if data.type == "Small Key":
            item_dungeon = item[:-10]
            if item_dungeon in world.dungeons.required_dungeons or item_dungeon == "Lanayru Caves" or not eud:
                progression_pool.extend([item] * data.quantity)
            else:
                useful_pool.extend([item] * data.quantity)

        if data.type == "Boss Key":
            item_dungeon = item[:-9]
            if item_dungeon in world.dungeons.required_dungeons or not eud:
                progression_pool.extend([item])
            else:
                useful_pool.extend([item])

        if data.type == "Map":
            filler_pool.extend([item])

    # Number of locations in the world (excluding Demise)
    num_items_left_to_place = len(world.multiworld.get_locations(world.player)) - 1

    # All progression items are added to the item pool.
    if len(progression_pool) > num_items_left_to_place:
        raise FillError(
            "There are insufficient locations to place progression items! "
            f"Trying to place {len(progression_pool)} items in only {num_items_left_to_place} locations."
        )
    pool.extend(progression_pool) # Should have more than enough locations available to place progression/useful items.
    pool.extend(useful_pool)
    num_items_left_to_place -= len(progression_pool)
    num_items_left_to_place -= len(useful_pool)

    starting_items.extend(_handle_starting_items(world))
    num_items_left_to_place += len(starting_items) # Since these items are removed from the pool, make sure they get filled.
    for itm in starting_items:
        pool.remove(itm)

    # Place useful items, then filler items to fill out the remaining locations.
    # Fill the remainder of the pool with weighted consumables
    num_consumables_needed = num_items_left_to_place - len(filler_pool)
    consumable_pool = world.multiworld.random.choices(
        list(CONSUMABLE_ITEMS.keys()),
        weights=list(CONSUMABLE_ITEMS.values()),
        k=num_consumables_needed
    )
    filler_pool.extend(consumable_pool)
    pool.extend(filler_pool)

    return pool, starting_items


def _handle_starting_items(world: "SSWorld") -> list[str]:
    """
    Handles starting items based on player's options.

    :return: A list of starting items.
    """
    options = world.options
    starting_items: list[str] = []

    # Starting Sword
    starting_sword_option = options.starting_sword.value
    for _ in range(int(starting_sword_option)):
        starting_items.append("Progressive Sword")
    
    # Starting Tablets
    starting_tablet_option = options.starting_tablet_count.value
    tablets = ["Emerald Tablet", "Ruby Tablet", "Amber Tablet"]
    if starting_tablet_option == 0:
        pass
    else:
        randomized_tablets = world.multiworld.random.sample(tablets, starting_tablet_option)
        starting_items.extend(randomized_tablets)

    # Starting Crystals
    starting_crystals_option = options.starting_crystal_packs.value
    for _ in range(int(starting_crystals_option)):
        starting_items.append("Gratitude Crystal Pack")

    # Starting Bottles
    starting_bottles_option = options.starting_bottles.value
    for _ in range(int(starting_bottles_option)):
        starting_items.append("Empty Bottle")

    # Starting HCs
    starting_hcs_option = options.starting_heart_containers.value
    for _ in range(int(starting_hcs_option)):
        starting_items.append("Heart Container")

    # Starting HPs
    starting_hps_option = options.starting_heart_pieces.value
    for _ in range(int(starting_hps_option)):
        starting_items.append("Heart Piece")

    # Starting Tadtones
    starting_tadtones_option = options.starting_tadtones.value
    for _ in range(int(starting_tadtones_option)):
        starting_items.append("Group of Tadtones")

    # Random Starting Item
    random_starting_item_option = bool(options.random_starting_item)
    if random_starting_item_option:
        rs_item = world.multiworld.random.choice(POSSIBLE_RANDOM_STARTING_ITEMS)
        starting_items.append(rs_item)

    # Start with Hylian Shield
    starting_hylian_option = bool(options.start_with_hylian_shield)
    if starting_hylian_option:
        starting_items.append("Hylian Shield")

    return starting_items


def _handle_placements(world: "SSWorld", pool: list[str]) -> list[str]:
    """
    Handles forced placements for items in certain locations based on player's options.

    :param world: The SS game world.
    :param pool: The item pool.
    :return: A list of items that are placed, to later be removed from the item pool.
    """

    options = world.options
    placed: list[str] = []

    # Place a "Victory" item on "Defeat Demise" for AP.
    world.get_location("Hylia's Realm - Defeat Demise").place_locked_item(world.create_item("Victory"))

    if not options.treasuresanity_in_silent_realms:
        for loc, data in LOCATION_TABLE.items():
            if data.type == SSLocType.RELIC:
                world.get_location(loc).place_locked_item(world.create_item("Dusk Relic"))
                placed.append("Dusk Relic")

    if not options.shopsanity:
        for loc, itm in BEEDLES_SHOP_VANILLA_ITEMS.items():
            world.get_location(loc).place_locked_item(world.create_item(itm))
            placed.append(itm)

    if not options.tadtonesanity:
        for loc, data in LOCATION_TABLE.items():
            if data.type == SSLocType.CLEF:
                world.get_location(loc).place_locked_item(world.create_item("Group of Tadtones"))
                placed.append("Group of Tadtones")

    if options.sword_dungeon_reward != "none":
        num_swords_to_place = pool.count("Progressive Sword")
        if num_swords_to_place < world.dungeons.required_dungeons:
            # More dungeons than swords to place, place as many as possible
            dungeons_to_place_swords = world.multiworld.random.sample(world.dungeons.required_dungeons, num_swords_to_place)
        elif num_swords_to_place >= world.dungeons.required_dungeons:
            # More swords than dungeons, so place a sword in each required dungeon
            dungeons_to_place_swords = world.dungeons.required_dungeons.copy()

        for dun in dungeons_to_place_swords:
            if options.sword_dungeon_reward == "heart_container":
                loc = DUNGEON_HC_CHECKS[dun]
            else:
                loc = DUNGEON_FINAL_CHECKS[dun]
            world.get_location(loc).place_locked_item(world.create_item("Progressive Sword"))
            placed.append("Progressive Sword")
    
    return placed


def item_classification(world: "SSWorld", name: str) -> IC | None:
    """
    Determine the item classification based on player's options.
    If no adjustment to classification, return None and use the classification specified in the item table.

    :param name: Name of the item
    :return: New IC of the item or None
    """

    adjusted_classification = None # TODO

    return adjusted_classification
