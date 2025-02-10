from typing import TYPE_CHECKING

from BaseClasses import ItemClassification as IC
from Fill import FillError
from Options import OptionError

from ..Items import ITEM_TABLE, CONSUMABLE_ITEMS
from ..Locations import LOCATION_TABLE, SSLocType, SSLocFlag
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
    world.starting_items = precollected_items

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
    vanilla_pool: list[str] = []
    for item, data in ITEM_TABLE.items():
        if data.type == "Item":
            adjusted_classification = item_classification(world, item)
            classification = (
                data.classification
                if adjusted_classification is None
                else adjusted_classification
            )

            if classification == IC.progression:
                progression_pool.extend([item] * data.quantity)
            elif classification == IC.useful:
                useful_pool.extend([item] * data.quantity)
            else:
                filler_pool.extend([item] * data.quantity)

        # Handle dungeon items
        if data.type in ["Small Key", "Boss Key", "Map"]:
            adjusted_classification = item_classification(world, item)
            classification = (
                data.classification
                if adjusted_classification is None
                else adjusted_classification
            )

            if classification == IC.progression:
                progression_pool.extend([item] * data.quantity)
            elif classification == IC.useful:
                useful_pool.extend([item] * data.quantity)
            else:
                filler_pool.extend([item] * data.quantity)

    if not world.options.rupeesanity:
        vanilla_pool.extend([data.vanilla_item for loc, data in LOCATION_TABLE.items() if data.flags & SSLocFlag.RUPEE])
            # Put in vanilla pool, so it bypasses rupoor filling
            # All rupees are consumables, so they weren't added to pools before
            # These will be removed from the pool and manually placed vanilla

    if not world.options.shopsanity:
        for loc, data in LOCATION_TABLE.items():
            if data.type == SSLocType.SHOP:
                itm = data.vanilla_item
                if ITEM_TABLE[itm].classification == IC.progression:
                    progression_pool.remove(itm)
                    vanilla_pool.append(itm)
                if ITEM_TABLE[itm].classification == IC.useful:
                    useful_pool.remove(itm)
                    vanilla_pool.append(itm)
                if ITEM_TABLE[itm].classification == IC.filler:
                    filler_pool.remove(itm)
                    vanilla_pool.append(itm)

    if not world.options.tadtonesanity:
        for loc, data in LOCATION_TABLE.items():
            if data.type == SSLocType.CLEF:
                itm = "Group of Tadtones"
                if itm in progression_pool:
                    progression_pool.remove(itm)
                    vanilla_pool.append(itm)
                elif itm in useful_pool:
                    useful_pool.remove(itm)
                    vanilla_pool.append(itm)
                elif itm in filler_pool:
                    filler_pool.remove(itm)
                    vanilla_pool.append(itm)

    if not world.options.treasuresanity_in_silent_realms:
        for loc, data in LOCATION_TABLE.items():
            if data.type == SSLocType.RELIC:
                itm = "Dusk Relic"
                filler_pool.remove(itm)
                vanilla_pool.append(itm)
    else:
        num_vanilla_relics = 10 - world.options.trial_treasure_amount.value
        for _ in range(num_vanilla_relics):
            itm = "Dusk Relic"
            filler_pool.remove(itm)
            vanilla_pool.append(itm)
        

    # Number of locations in the world (excluding Demise)
    num_items_left_to_place = len(world.multiworld.get_locations(world.player)) - 1

    # All progression items are added to the item pool.
    if len(progression_pool) > num_items_left_to_place:
        raise FillError(
            "There are insufficient locations to place progression items! "
            f"Trying to place {len(progression_pool)} items in only {num_items_left_to_place} locations."
        )
    
    # Should have more than enough locations available to place progression/useful/vanilla items.
    pool.extend(progression_pool)
    pool.extend(useful_pool)
    pool.extend(vanilla_pool)
    num_items_left_to_place -= len(progression_pool)
    num_items_left_to_place -= len(useful_pool)
    num_items_left_to_place -= len(vanilla_pool)

    starting_items.extend(_handle_starting_items(world))
    num_items_left_to_place += len(
        starting_items
    )  # Since these items are removed from the pool, make sure they get filled.
    for itm in starting_items:
        if itm in ["Heart Container", "Heart Piece"]:
            filler_pool.remove(itm)
        else:
            pool.remove(itm)
            
    # Gondo's upgrades will be removed from the pool if unrandomized, so in that case
    # we want to add another 6 consumables
    if not world.options.gondo_upgrades:
        num_items_left_to_place += 6

    # Now fill the rest of the filler pool with consumables
    num_consumables_needed = num_items_left_to_place - len(filler_pool)
    consumable_pool = []

    consumable_pool.extend(world.multiworld.random.choices(
        list(CONSUMABLE_ITEMS.keys()),
        weights=list(CONSUMABLE_ITEMS.values()),
        k=num_consumables_needed,
    ))
    filler_pool.extend(consumable_pool)
    world.multiworld.random.shuffle(filler_pool)

    # Now fill rupoors
    if world.options.rupoor_mode == "added":
        if len(filler_pool) < 15:
            filler_pool = ["Rupoor"] * len(filler_pool)
            # Replace the entire filler pool with rupoors
        else:
            for i in range(15):
                filler_pool[i] = "Rupoor"
            # Replace the first 15 elements with rupoors
    elif world.options.rupoor_mode == "rupoor_mayhem":
        for i in range(round(len(filler_pool)/2)):
            filler_pool[i] = "Rupoor"
        # Replace the first half of the pool with rupoors
    elif world.options.rupoor_mode == "rupoor_insanity":
        filler_pool = ["Rupoor"] * len(filler_pool)
        # Replace the entire filler pool with rupoors

    world.multiworld.random.shuffle(filler_pool)
    pool.extend(filler_pool)

    return pool, starting_items


def _handle_starting_items(world: "SSWorld") -> list[str]:
    """
    Handles starting items based on player's options.

    :return: A list of starting items.
    """
    options = world.options
    starting_items: list[str] = []

    # General Starting Items
    starting_items_option = options.starting_items
    for itm, q in starting_items_option.value.items():
        if itm in ITEM_TABLE:
            if q > ITEM_TABLE[itm].quantity:
                raise OptionError(
                    f"Too many starting items! Tried to give {q} {itm} but could only give {ITEM_TABLE[itm].quantity}"
                )
            else:
                starting_items.extend([itm] * q)
        else:
            raise OptionError(f"Unknown item in option `starting items`: {itm}")

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
        randomized_tablets = world.multiworld.random.sample(
            tablets, starting_tablet_option
        )
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
        possible_items_to_give = []
        for itm in POSSIBLE_RANDOM_STARTING_ITEMS:
            possible_items_to_give.extend([itm] * ITEM_TABLE[itm].quantity)
        for itm in starting_items:
            if itm in possible_items_to_give:
                # Here we make sure our starting items don't collide with the random starting item
                possible_items_to_give.remove(itm)
        if len(possible_items_to_give) == 0:
            raise OptionError("Tried to give a random starting item, but couldn't find any items to give.")
        rs_item = world.multiworld.random.choice(possible_items_to_give)
        starting_items.append(rs_item)

    # Start with Hylian Shield
    starting_hylian_option = bool(options.start_with_hylian_shield)
    if starting_hylian_option:
        starting_items.append("Hylian Shield")

    # starting_items.extend(world.options.starting_items)

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
    world.get_location("Hylia's Realm - Defeat Demise").place_locked_item(
        world.create_item("Victory")
    )

    if not options.treasuresanity_in_silent_realms:
        for loc, data in LOCATION_TABLE.items():
            if data.type == SSLocType.RELIC:
                world.get_location(loc).place_locked_item(
                    world.create_item("Dusk Relic")
                )
                placed.append("Dusk Relic")
    else:
        num_relics = options.trial_treasure_amount.value
        for trl in TRIAL_LIST:
            all_relics = [loc for loc in world.multiworld.get_locations(world.player) if loc.parent_region == world.get_region(trl) and loc.type == SSLocType.RELIC]
            relics_to_place = world.multiworld.random.sample(all_relics, 10 - num_relics)
            for rel in relics_to_place:
                rel.place_locked_item(world.create_item("Dusk Relic"))
                placed.append("Dusk Relic")

    if not options.shopsanity:
        for loc, data in LOCATION_TABLE.items():
            if data.type == SSLocType.SHOP:
                world.get_location(loc).place_locked_item(
                    world.create_item(data.vanilla_item)
                )
                placed.append(data.vanilla_item)

    if not options.tadtonesanity:
        for loc, data in LOCATION_TABLE.items():
            if data.type == SSLocType.CLEF:
                world.get_location(loc).place_locked_item(
                    world.create_item("Group of Tadtones")
                )
                placed.append("Group of Tadtones")

    if not options.rupeesanity:
        for loc, data in LOCATION_TABLE.items():
            if data.flags & SSLocFlag.RUPEE:
                world.get_location(loc).place_locked_item(
                    world.create_item(data.vanilla_item)
                )
                placed.append(data.vanilla_item)

    if options.sword_dungeon_reward != "none":
        num_swords_to_place = pool.count("Progressive Sword")
        if num_swords_to_place < len(world.dungeons.required_dungeons):
            # More dungeons than swords to place, place as many as possible
            dungeons_to_place_swords = world.multiworld.random.sample(
                world.dungeons.required_dungeons, num_swords_to_place
            )
        elif num_swords_to_place >= len(world.dungeons.required_dungeons):
            # More swords than dungeons, so place a sword in each required dungeon
            dungeons_to_place_swords = world.dungeons.required_dungeons.copy()

        for dun in dungeons_to_place_swords:
            if options.sword_dungeon_reward == "heart_container":
                loc = DUNGEON_HC_CHECKS[dun]
            else:
                loc = DUNGEON_FINAL_CHECKS[dun]
            world.get_location(loc).place_locked_item(
                world.create_item("Progressive Sword")
            )
            placed.append("Progressive Sword")

    if options.triforce_shuffle == "vanilla":
        world.get_location("Sky Keep - Sacred Power of Din").place_locked_item(world.create_item("Triforce of Power"))
        world.get_location("Sky Keep - Sacred Power of Nayru").place_locked_item(world.create_item("Triforce of Wisdom"))
        world.get_location("Sky Keep - Sacred Power of Farore").place_locked_item(world.create_item("Triforce of Courage"))
        placed.extend(["Triforce of Power", "Triforce of Wisdom", "Triforce of Courage"])
    elif options.triforce_shuffle == "sky_keep":
        locations_to_place = [loc for loc in world.multiworld.get_locations(world.player) if loc.parent_region == world.get_region("Sky Keep")]
        triforce_locations = world.multiworld.random.sample(locations_to_place, 3)
        world.multiworld.random.shuffle(triforce_locations)
        for i, tri in enumerate(["Triforce of Power", "Triforce of Wisdom", "Triforce of Courage"]):
            triforce_locations[i].place_locked_item(world.create_item(tri))
        placed.extend(["Triforce of Power", "Triforce of Wisdom", "Triforce of Courage"])

    if not options.gondo_upgrades:
        placed.extend(GONDO_UPGRADES)
        # We're not actually going to place these in the world, the rando will patch them in
        # Still, remove them from the item pool

    return placed


def item_classification(world: "SSWorld", name: str) -> IC | None:
    """
    Determine the item classification based on player's options.
    If no adjustment to classification, return None and use the classification specified in the item table.

    :param name: Name of the item
    :return: New IC of the item or None
    """
    adjusted_classification = None
    item_type = ITEM_TABLE[name].type

    # Dungeon Entrance Access Items
    if world.options.randomize_entrances == "none" and world.options.empty_unrequired_dungeons:
        if "Earth Temple" not in world.dungeons.required_dungeons:
            if name == "Key Piece":
                adjusted_classification = IC.filler
        if "Sandship" not in world.dungeons.required_dungeons:
            if name == "Sea Chart":
                adjusted_classification = IC.filler
        if not world.options.triforce_required or world.options.triforce_shuffle == "anywhere":
            if name == "Stone of Trials":
                adjusted_classification = IC.filler
    
    # Dungeon Items
    if world.options.empty_unrequired_dungeons and item_type in ["Map", "Small Key", "Boss Key"]:
        if item_type == "Map":
            item_dungeon = name[:-4]
            if item_dungeon == "Sky Keep":
                adjusted_classification = IC.filler if world.options.triforce_shuffle == "anywhere" else None
            elif not item_dungeon in world.dungeons.required_dungeons:
                adjusted_classification = IC.filler
                # If map not a required dungeon, make it filler
                # Otherwise, it will be useful
        if item_type == "Small Key":
            item_dungeon = name[:-10]
            if item_dungeon == "Sky Keep":
                adjusted_classification = IC.filler if world.options.triforce_shuffle == "anywhere" else None
            elif item_dungeon == "Lanayru Caves":
                pass
                # Caves key will always stay progression
            elif not item_dungeon in world.dungeons.required_dungeons:
                adjusted_classification = IC.filler
                # If small key not a required dungeon, make it filler
                # Otherwise, it will be progression
        if item_type == "Boss Key":
            item_dungeon = name[:-9]
            if not item_dungeon in world.dungeons.required_dungeons:
                adjusted_classification = IC.filler
                # If boss key not a required dungeon, make it filler
                # Otherwise, it will be progression

    # Swords
    if world.options.starting_sword.value >= world.options.got_sword_requirement.value + 2:
        if name == "Progressive Sword":
            adjusted_classification = IC.useful
            # If our starting sword is equal to or greater than the required sword, make
            # progressive swords useful rather than progression

    # Triforces
    if not world.options.triforce_required:
        if "Triforce" in name:
            adjusted_classification = IC.useful
            # If Triforce is not required, make it useful
    
    # Pouches
    if "Progressive Pouch" in world.options.starting_items:
        if name == "Progressive Pouch":
            adjusted_classification = IC.useful
            # If we start with a pouch, then further upgrades will be useful rather
            # than progression

    # Items for single checks
    if "Upper Skyloft - Ghost/Pipit's Crystals" in world.options.exclude_locations:
        if name == "Cawlin's Letter":
            adjusted_classification = IC.filler
    if "Skyloft Village - Bertie's Crystals" in world.options.exclude_locations:
        if name == "Baby Rattle":
            adjusted_classification = IC.filler
    if "Sky - Beedle's Crystals" in world.options.exclude_locations:
        if name == "Horned Colossus Beetle":
            adjusted_classification = IC.filler
    if "Lanayru Gorge - Thunder Dragon's Reward" in world.options.exclude_locations:
        if name == "Life Tree Fruit":
            adjusted_classification = IC.filler
    if "Flooded Faron Woods - Water Dragon's Reward" in world.options.exclude_locations:
        if name == "Group of Tadtones":
            adjusted_classification = IC.filler

    return adjusted_classification
