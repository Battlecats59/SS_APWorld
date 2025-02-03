from enum import Enum, Flag, auto
from typing import TYPE_CHECKING, NamedTuple, Optional

from BaseClasses import Location, Region


class SSLocFlag(Flag):
    """
    Flags to categorize checks.
    Used for logic purposes and to determine progression based on options.
    """

    ALWAYS = auto()
    GODDESS = auto()
    CRYSTAL = auto()
    SCRAPPR = auto()
    MINIGME = auto()
    BEEDLE = auto()
    BTREAUX = auto()
    RUPEE = auto()
    TRIAL = auto()  # Used for relics
    TADTONE = auto()

    D_SV = auto()
    D_ET = auto()
    D_LMF = auto()
    D_AC = auto()
    D_SSH = auto()
    D_FS = auto()
    D_SK = auto()


class SSLocType(Enum):
    """
    Types of checks.
    """

    T_BOX = auto()
    ITEM = auto()
    EVENT = auto()
    SHOP = auto()
    HRTCO = auto()
    SOIL = auto()  # Digging spot
    CLEF = auto()  # Tadtone note
    SWSB = auto()  # IoS Crest
    WPOBJ = auto()
    RELIC = auto()
    BELL = auto()
    CHEST = auto()  # THIS IS **NOT** THE STANDARD CHEST. THIS IS FOR ZELDA'S CLOSET.
    # Use T_BOX for checks in chests.
    CHAND = auto()  # Chandelier
    EBC = auto()  # Item taken from enemy with whip


class SSLocCheckedFlag(Flag):
    """
    Either scene flag or story flag. Determines what is checked to see
    if the location has been checked by the player.

    Special [SPECL] flag may require checking multiple flags. Flags are hardcoded during
    flag checking.
    """

    STORY = auto()
    SCENE = auto()
    SPECL = auto()


class SSLocData(NamedTuple):
    """
    Class contains data for any location in SS.
    """

    code: Optional[int]
    flags: SSLocFlag
    region: str
    stage: str
    type: SSLocType
    checked_flag: list[
        SSLocCheckedFlag, int, int, any
    ]  # [ Flag_type, flag_bit (0x0-0xF), flag_value (0x01-0x80), scene (string) OR story flag address (ending in zero)]


class SSLocation(Location):
    """
    Class represents a location in SS.
    """

    game: str = "Skyward Sword"

    def __init__(self, player: int, name: str, parent: Region, data: SSLocData):
        address = None if data.code is None else SSLocation.get_apid(data.code)
        super().__init__(player, name, address=address, parent=parent)

        self.code = data.code
        self.flags = data.flags
        self.region = data.region
        self.stage = data.stage
        self.type = data.type
        self.checked_flag = data.checked_flag
        self.address = self.address

    @staticmethod
    def get_apid(code: int) -> int:
        """
        Compute the Archipelago ID for the given location index.

        :param code: The index of the location.
        :return: The computed Archipelago ID.
        """
        base_id: int = 98000
        return base_id + code


LOCATION_TABLE: dict[str, SSLocData] = {
    "Upper Skyloft - Fledge's Gift": SSLocData(
        0,
        SSLocFlag.ALWAYS,
        "Upper Skyloft",
        "F001r",
        SSLocType.EVENT,
        [SSLocCheckedFlag.STORY, 0xF, 0x02, 0x805A9B30],  # Flag 923
    ),
    "Upper Skyloft - Owlan's Gift": SSLocData(
        1,
        SSLocFlag.ALWAYS,
        "Upper Skyloft",
        "F000",
        SSLocType.EVENT,
        [SSLocCheckedFlag.SCENE, 0x3, 0x10, "Skyloft"],
    ),
    "Upper Skyloft - Sparring Hall Chest": SSLocData(
        2,
        SSLocFlag.ALWAYS,
        "Upper Skyloft",
        "F009r",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0x1, 0x04, "Skyloft"],
    ),
    "Upper Skyloft - Ring Knight Academy Bell": SSLocData(
        3,
        SSLocFlag.RUPEE,
        "Upper Skyloft",
        "F000",
        SSLocType.BELL,
        [SSLocCheckedFlag.SCENE, 0xF, 0x20, "Skyloft"],
    ),
    "Upper Skyloft - Chest near Goddess Statue": SSLocData(
        4,
        SSLocFlag.ALWAYS,
        "Upper Skyloft",
        "F000",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0xF, 0x80, "Skyloft"],
    ),
    "Upper Skyloft - First Goddess Sword Item in Goddess Statue": SSLocData(
        5,
        SSLocFlag.ALWAYS,
        "Upper Skyloft",
        "F008r",
        SSLocType.EVENT,
        [SSLocCheckedFlag.STORY, 0x0, 0x20, 0x805A9B40],  # Flag 951
    ),
    "Upper Skyloft - Second Goddess Sword Item in Goddess Statue": SSLocData(
        6,
        SSLocFlag.ALWAYS,
        "Upper Skyloft",
        "F008r",
        SSLocType.EVENT,
        [SSLocCheckedFlag.STORY, 0x0, 0x20, 0x805A9B40],  # Flag 951
    ),
    "Upper Skyloft - In Zelda's Closet": SSLocData(
        7,
        SSLocFlag.ALWAYS,
        "Upper Skyloft",
        "F001r",
        SSLocType.CHEST,
        [SSLocCheckedFlag.SCENE, 0x5, 0x01, "Skyloft"],
    ),
    "Upper Skyloft - Owlan's Crystals": SSLocData(
        8,
        SSLocFlag.SCRAPPR,
        "Upper Skyloft",
        "F001r",
        SSLocType.EVENT,
        [SSLocCheckedFlag.STORY, 0x1, 0x40, 0x805A9B10],  # Flag 482
    ),
    "Upper Skyloft - Fledge's Crystals": SSLocData(
        9,
        SSLocFlag.CRYSTAL,
        "Upper Skyloft",
        "F001r",
        SSLocType.EVENT,
        [SSLocCheckedFlag.STORY, 0xC, 0x10, 0x805A9B00],  # Flag 394
    ),
    "Upper Skyloft - Item from Cawlin": SSLocData(
        10,
        SSLocFlag.ALWAYS,
        "Upper Skyloft",
        "F001r",
        SSLocType.EVENT,
        [SSLocCheckedFlag.STORY, 0xF, 0x04, 0x805A9B30],  # Flag 924
    ),
    "Upper Skyloft - Ghost/Pipit's Crystals": SSLocData(
        11,
        SSLocFlag.CRYSTAL,
        "Upper Skyloft",
        "F001r",
        SSLocType.EVENT,
        [
            SSLocCheckedFlag.SPECL,
            0x0,
            0x0,
            0x0,
        ],  # SPECIAL - 2 story flags, determined later; index 0x0
    ),
    "Upper Skyloft - Pumpkin Archery -- 600 Points": SSLocData(
        12,
        SSLocFlag.MINIGME,
        "Upper Skyloft",
        "F000",
        SSLocType.EVENT,
        [SSLocCheckedFlag.STORY, 0x0, 0x20, 0x805A9B00],  # Flag 359
    ),
    # Central Skyloft
    "Central Skyloft - Potion Lady's Gift": SSLocData(
        13,
        SSLocFlag.ALWAYS,
        "Central Skyloft",
        "F004r",
        SSLocType.EVENT,
        [SSLocCheckedFlag.STORY, 0xD, 0x08, 0x805A9AD0],  # Flag 35
    ),
    "Central Skyloft - Repair Gondo's Junk": SSLocData(
        14,
        SSLocFlag.ALWAYS,
        "Central Skyloft",
        "F004r",
        SSLocType.EVENT,
        [SSLocCheckedFlag.STORY, 0xF, 0x01, 0x805A9AF0],  # Flag 322 (Repurposed)
    ),
    "Central Skyloft - Wryna's Crystals": SSLocData(
        15,
        SSLocFlag.CRYSTAL,
        "Central Skyloft",
        "F006r",
        SSLocType.EVENT,
        [SSLocCheckedFlag.STORY, 0xF, 0x10, 0x805A9AF0],  # Flag 326
    ),
    "Central Skyloft - Waterfall Cave First Chest": SSLocData(
        16,
        SSLocFlag.ALWAYS,
        "Central Skyloft",
        "D000",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0xE, 0x80, "Skyloft"],
    ),
    "Central Skyloft - Waterfall Cave Second Chest": SSLocData(
        17,
        SSLocFlag.ALWAYS,
        "Central Skyloft",
        "D000",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0xE, 0x40, "Skyloft"],
    ),
    "Central Skyloft - Rupee Waterfall Cave Crawlspace": SSLocData(
        18,
        SSLocFlag.ALWAYS,
        "Central Skyloft",
        "D000",
        SSLocType.ITEM,
        [SSLocCheckedFlag.SCENE, 0xA, 0x01, "Skyloft"],
    ),
    "Central Skyloft - Parrow's Gift": SSLocData(
        19,
        SSLocFlag.ALWAYS,
        "Central Skyloft",
        "F000",
        SSLocType.EVENT,
        [SSLocCheckedFlag.STORY, 0xD, 0x01, 0x805A9B00],  # Flag 382
    ),
    "Central Skyloft - Parrow's Crystals": SSLocData(
        20,
        SSLocFlag.CRYSTAL,
        "Central Skyloft",
        "F000",
        SSLocType.EVENT,
        [SSLocCheckedFlag.STORY, 0xD, 0x04, 0x805A9B00],  # Flag 384
    ),
    "Central Skyloft - Peater/Peatrice's Crystals": SSLocData(
        21,
        SSLocFlag.CRYSTAL,
        "Central Skyloft",
        "F018r",
        SSLocType.EVENT,
        [
            SSLocCheckedFlag.SPECL,
            0x1,
            0x0,
            0x0,
        ],  # SPECIAL - 2 flags, determined later; index 0x1
    ),
    "Central Skyloft - Item in Bird Nest": SSLocData(
        22,
        SSLocFlag.ALWAYS,
        "Central Skyloft",
        "F000",
        SSLocType.ITEM,
        [SSLocCheckedFlag.SCENE, 0x0, 0x20, "Skyloft"],
    ),
    "Central Skyloft - Shed Chest": SSLocData(
        23,
        SSLocFlag.ALWAYS,
        "Central Skyloft",
        "F000",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0xF, 0x40, "Skyloft"],
    ),
    "Central Skyloft - West Cliff Goddess Chest": SSLocData(
        24,
        SSLocFlag.GODDESS,
        "Central Skyloft",
        "F000",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0xC, 0x08, "Skyloft"],
    ),
    "Central Skyloft - Bazaar Goddess Chest": SSLocData(
        25,
        SSLocFlag.GODDESS,
        "Central Skyloft",
        "F004r",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0xC, 0x02, "Skyloft"],
    ),
    "Central Skyloft - Shed Goddess Chest": SSLocData(
        26,
        SSLocFlag.GODDESS,
        "Central Skyloft",
        "F000",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0xB, 0x04, "Skyloft"],
    ),
    "Central Skyloft - Floating Island Goddess Chest": SSLocData(
        27,
        SSLocFlag.GODDESS,
        "Central Skyloft",
        "F000",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0xB, 0x02, "Skyloft"],
    ),
    "Central Skyloft - Waterfall Goddess Chest": SSLocData(
        28,
        SSLocFlag.GODDESS,
        "Central Skyloft",
        "F000",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0xB, 0x01, "Skyloft"],
    ),
    # Skyloft Village
    "Skyloft Village - Mallara's Crystals": SSLocData(
        29,
        SSLocFlag.CRYSTAL,
        "Skyloft Village",
        "F016r",
        SSLocType.EVENT,
        [SSLocCheckedFlag.STORY, 0x8, 0x40, 0x805A9B10],  # Flag 575
    ),
    "Skyloft Village - Bertie's Crystals": SSLocData(
        30,
        SSLocFlag.CRYSTAL,
        "Skyloft Village",
        "F014r",
        SSLocType.EVENT,
        [SSLocCheckedFlag.STORY, 0xD, 0x20, 0x805A9B00],  # Flag 387
    ),
    "Skyloft Village - Sparrot's Crystals": SSLocData(
        31,
        SSLocFlag.SCRAPPR,
        "Skyloft Village",
        "F013r",
        SSLocType.EVENT,
        [SSLocCheckedFlag.STORY, 0x2, 0x08, 0x805A9B00],  # Flag 373
    ),
    # Batreaux's House
    "Batreaux's House - 5 Crystals": SSLocData(
        32,
        SSLocFlag.BTREAUX,
        "Batreaux's House",
        "F012r",
        SSLocType.EVENT,
        [SSLocCheckedFlag.SCENE, 0x9, 0x40, "Skyloft"],
    ),
    "Batreaux's House - 10 Crystals": SSLocData(
        33,
        SSLocFlag.BTREAUX,
        "Batreaux's House",
        "F012r",
        SSLocType.EVENT,
        [SSLocCheckedFlag.SCENE, 0x9, 0x80, "Skyloft"],
    ),
    "Batreaux's House - 30 Crystals": SSLocData(
        34,
        SSLocFlag.BTREAUX,
        "Batreaux's House",
        "F012r",
        SSLocType.EVENT,
        [SSLocCheckedFlag.SCENE, 0x8, 0x01, "Skyloft"],
    ),
    "Batreaux's House - 30 Crystals Chest": SSLocData(
        35,
        SSLocFlag.BTREAUX,
        "Batreaux's House",
        "F012r",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0xA, 0x20, "Skyloft"],
    ),
    "Batreaux's House - 40 Crystals": SSLocData(
        36,
        SSLocFlag.BTREAUX,
        "Batreaux's House",
        "F012r",
        SSLocType.EVENT,
        [SSLocCheckedFlag.SCENE, 0x8, 0x02, "Skyloft"],
    ),
    "Batreaux's House - 50 Crystals": SSLocData(
        37,
        SSLocFlag.BTREAUX,
        "Batreaux's House",
        "F012r",
        SSLocType.EVENT,
        [SSLocCheckedFlag.SCENE, 0x8, 0x04, "Skyloft"],
    ),
    "Batreaux's House - 70 Crystals": SSLocData(
        38,
        SSLocFlag.BTREAUX,
        "Batreaux's House",
        "F012r",
        SSLocType.EVENT,
        [SSLocCheckedFlag.SCENE, 0x8, 0x08, "Skyloft"],
    ),
    "Batreaux's House - 70 Crystals Second Reward": SSLocData(
        39,
        SSLocFlag.BTREAUX,
        "Batreaux's House",
        "F012r",
        SSLocType.EVENT,
        [SSLocCheckedFlag.SCENE, 0x8, 0x08, "Skyloft"],
    ),
    "Batreaux's House - 80 Crystals": SSLocData(
        40,
        SSLocFlag.BTREAUX,
        "Batreaux's House",
        "F012r",
        SSLocType.EVENT,
        [SSLocCheckedFlag.SCENE, 0x8, 0x80, "Skyloft"],  # TODO: check
    ),
    # Beedle's Shop
    "Beedle's Shop - 300 Rupee Item": SSLocData(
        41,
        SSLocFlag.BEEDLE,
        "Beedle's Shop",
        "F002r",
        SSLocType.SHOP,
        [SSLocCheckedFlag.STORY, 0x3, 0x01, 0x805A9B40],  # Flag 954
    ),
    "Beedle's Shop - 600 Rupee Item": SSLocData(
        42,
        SSLocFlag.BEEDLE,
        "Beedle's Shop",
        "F002r",
        SSLocType.SHOP,
        [SSLocCheckedFlag.STORY, 0x3, 0x02, 0x805A9B40],  # Flag 955
    ),
    "Beedle's Shop - 1200 Rupee Item": SSLocData(
        43,
        SSLocFlag.BEEDLE,
        "Beedle's Shop",
        "F002r",
        SSLocType.SHOP,
        [SSLocCheckedFlag.STORY, 0x3, 0x04, 0x805A9B40],  # Flag 956
    ),
    "Beedle's Shop - 800 Rupee Item": SSLocData(
        44,
        SSLocFlag.BEEDLE,
        "Beedle's Shop",
        "F002r",
        SSLocType.SHOP,
        [SSLocCheckedFlag.STORY, 0x3, 0x08, 0x805A9B40],  # Flag 957
    ),
    "Beedle's Shop - 1600 Rupee Item": SSLocData(
        45,
        SSLocFlag.BEEDLE,
        "Beedle's Shop",
        "F002r",
        SSLocType.SHOP,
        [SSLocCheckedFlag.STORY, 0x3, 0x10, 0x805A9B40],  # Flag 958
    ),
    "Beedle's Shop - First 100 Rupee Item": SSLocData(
        46,
        SSLocFlag.BEEDLE,
        "Beedle's Shop",
        "F002r",
        SSLocType.SHOP,
        [SSLocCheckedFlag.STORY, 0xE, 0x80, 0x805A9B30],  # Flag 937
    ),
    "Beedle's Shop - Second 100 Rupee Item": SSLocData(
        47,
        SSLocFlag.BEEDLE,
        "Beedle's Shop",
        "F002r",
        SSLocType.SHOP,
        [SSLocCheckedFlag.STORY, 0x1, 0x01, 0x805A9B40],  # Flag 938
    ),
    "Beedle's Shop - Third 100 Rupee Item": SSLocData(
        48,
        SSLocFlag.BEEDLE,
        "Beedle's Shop",
        "F002r",
        SSLocType.SHOP,
        [SSLocCheckedFlag.STORY, 0x1, 0x02, 0x805A9B40],  # Flag 939
    ),
    "Beedle's Shop - 50 Rupee Item": SSLocData(
        49,
        SSLocFlag.BEEDLE,
        "Beedle's Shop",
        "F002r",
        SSLocType.SHOP,
        [SSLocCheckedFlag.STORY, 0x1, 0x04, 0x805A9B40],  # Flag 940
    ),
    "Beedle's Shop - 1000 Rupee Item": SSLocData(
        50,
        SSLocFlag.BEEDLE,
        "Beedle's Shop",
        "F002r",
        SSLocType.SHOP,
        [SSLocCheckedFlag.STORY, 0x1, 0x08, 0x805A9B40],  # Flag 941
    ),
    # Sky
    "Sky - Lumpy Pumpkin - Chandelier": SSLocData(
        51,
        SSLocFlag.ALWAYS,
        "Sky",
        "F011r",
        SSLocType.CHAND,
        [SSLocCheckedFlag.SCENE, 0x1, 0x80, "Sky"],
    ),
    "Sky - Lumpy Pumpkin - Harp Minigame": SSLocData(
        52,
        SSLocFlag.MINIGME,
        "Sky",
        "F011r",
        SSLocType.EVENT,
        [SSLocCheckedFlag.STORY, 0xD, 0x04, 0x805A9AF0],  # Flag 296
    ),
    "Sky - Kina's Crystals": SSLocData(
        53,
        SSLocFlag.SCRAPPR,
        "Sky",
        "F020",
        SSLocType.EVENT,
        [SSLocCheckedFlag.STORY, 0xE, 0x10, 0x805A9B00],  # Flag 472
    ),
    "Sky - Orielle's Crystals": SSLocData(
        54,
        SSLocFlag.CRYSTAL,
        "Sky",
        "F020",
        SSLocType.EVENT,
        [SSLocCheckedFlag.STORY, 0xD, 0x02, 0x805A9B00],  # Flag 383
    ),
    "Sky - Beedle's Crystals": SSLocData(
        55,
        SSLocFlag.CRYSTAL,
        "Sky",
        "F020",
        SSLocType.EVENT,
        [SSLocCheckedFlag.STORY, 0x1, 0x02, 0x805A9B10],  # Flag 477
    ),
    "Sky - Dodoh's Crystals": SSLocData(
        56,
        SSLocFlag.SCRAPPR,
        "Sky",
        "F020",
        SSLocType.EVENT,
        [SSLocCheckedFlag.STORY, 0xE, 0x01, 0x805A9B00],  # Flag 398
    ),
    "Sky - Fun Fun Island Minigame -- 500 Rupees": SSLocData(
        57,
        SSLocFlag.MINIGME,
        "Sky",
        "F020",
        SSLocType.EVENT,
        [SSLocCheckedFlag.SCENE, 0x3, 0x08, "Sky"],
    ),
    "Sky - Chest in Breakable Boulder near Fun Fun Island": SSLocData(
        58,
        SSLocFlag.ALWAYS,
        "Sky",
        "F020",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0x8, 0x08, "Sky"],
    ),
    "Sky - Chest in Breakable Boulder near Lumpy Pumpkin": SSLocData(
        59,
        SSLocFlag.ALWAYS,
        "Sky",
        "F020",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0x8, 0x04, "Sky"],
    ),
    "Sky - Bamboo Island Goddess Chest": SSLocData(
        60,
        SSLocFlag.GODDESS,
        "Sky",
        "F020",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0xF, 0x08, "Sky"],
    ),
    "Sky - Goddess Chest on Island next to Bamboo Island": SSLocData(
        61,
        SSLocFlag.GODDESS,
        "Sky",
        "F020",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0xF, 0x04, "Sky"],
    ),
    "Sky - Goddess Chest in Cave on Island next to Bamboo Island": SSLocData(
        62,
        SSLocFlag.GODDESS,
        "Sky",
        "F020",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0xF, 0x02, "Sky"],
    ),
    "Sky - Beedle's Island Goddess Chest": SSLocData(
        63,
        SSLocFlag.GODDESS,
        "Sky",
        "F020",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0xF, 0x01, "Sky"],
    ),
    "Sky - Beedle's Island Cage Goddess Chest": SSLocData(
        64,
        SSLocFlag.GODDESS,
        "Sky",
        "F020",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0xE, 0x08, "Sky"],
    ),
    "Sky - Northeast Island Goddess Chest behind Bombable Rocks": SSLocData(
        65,
        SSLocFlag.GODDESS,
        "Sky",
        "F020",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0xE, 0x04, "Sky"],
    ),
    "Sky - Northeast Island Cage Goddess Chest": SSLocData(
        66,
        SSLocFlag.GODDESS,
        "Sky",
        "F020",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0xE, 0x02, "Sky"],
    ),
    "Sky - Lumpy Pumpkin - Goddess Chest on the Roof": SSLocData(
        67,
        SSLocFlag.GODDESS,
        "Sky",
        "F020",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0xE, 0x01, "Sky"],
    ),
    "Sky - Lumpy Pumpkin - Outside Goddess Chest": SSLocData(
        68,
        SSLocFlag.GODDESS,
        "Sky",
        "F020",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0xD, 0x08, "Sky"],
    ),
    "Sky - Goddess Chest on Island Closest to Faron Pillar": SSLocData(
        69,
        SSLocFlag.GODDESS,
        "Sky",
        "F020",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0xD, 0x04, "Sky"],
    ),
    "Sky - Goddess Chest outside Volcanic Island": SSLocData(
        70,
        SSLocFlag.GODDESS,
        "Sky",
        "F020",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0xD, 0x02, "Sky"],
    ),
    "Sky - Goddess Chest inside Volcanic Island": SSLocData(
        71,
        SSLocFlag.GODDESS,
        "Sky",
        "F020",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0xD, 0x01, "Sky"],
    ),
    "Sky - Goddess Chest under Fun Fun Island": SSLocData(
        72,
        SSLocFlag.GODDESS,
        "Sky",
        "F020",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0xC, 0x08, "Sky"],
    ),
    "Sky - Southwest Triple Island Upper Goddess Chest": SSLocData(
        73,
        SSLocFlag.GODDESS,
        "Sky",
        "F020",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0xC, 0x04, "Sky"],
    ),
    "Sky - Southwest Triple Island Lower Goddess Chest": SSLocData(
        74,
        SSLocFlag.GODDESS,
        "Sky",
        "F020",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0xC, 0x02, "Sky"],
    ),
    "Sky - Southwest Triple Island Cage Goddess Chest": SSLocData(
        75,
        SSLocFlag.GODDESS,
        "Sky",
        "F020",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0xC, 0x01, "Sky"],
    ),
    # Thunderhead
    "Thunderhead - Isle of Songs - Strike Crest with Goddess Sword": SSLocData(
        76,
        SSLocFlag.ALWAYS,
        "Thunderhead",
        "F010r",
        SSLocType.SWSB,
        [SSLocCheckedFlag.SCENE, 0x7, 0x04, "Sky"],  # CHECKTHIS
    ),
    "Thunderhead - Isle of Songs - Strike Crest with Longsword": SSLocData(
        77,
        SSLocFlag.ALWAYS,
        "Thunderhead",
        "F010r",
        SSLocType.SWSB,
        [SSLocCheckedFlag.SCENE, 0x7, 0x08, "Sky"],  # CHECKTHIS
    ),
    "Thunderhead - Isle of Songs - Strike Crest with White Sword": SSLocData(
        78,
        SSLocFlag.ALWAYS,
        "Thunderhead",
        "F010r",
        SSLocType.SWSB,
        [SSLocCheckedFlag.SCENE, 0x7, 0x10, "Sky"],  # CHECKTHIS
    ),
    "Thunderhead - Song from Levias": SSLocData(
        79,
        SSLocFlag.ALWAYS,
        "Thunderhead",
        "F023",
        SSLocType.EVENT,
        [SSLocCheckedFlag.STORY, 0xE, 0x10, 0x805A9B30],  # Flag 934
    ),
    "Thunderhead - Bug Heaven -- 10 Bugs in 3 Minutes": SSLocData(
        80,
        SSLocFlag.MINIGME,
        "Thunderhead",
        "F023",
        SSLocType.EVENT,
        [SSLocCheckedFlag.STORY, 0xF, 0x08, 0x805A9B30],  # Flag 925
    ),
    "Thunderhead - East Island Chest": SSLocData(
        81,
        SSLocFlag.ALWAYS,
        "Thunderhead",
        "F023",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0x8, 0x02, "Sky"],
    ),
    "Thunderhead - East Island Goddess Chest": SSLocData(
        82,
        SSLocFlag.GODDESS,
        "Thunderhead",
        "F023",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0xB, 0x08, "Sky"],
    ),
    "Thunderhead - Goddess Chest on top of Isle of Songs": SSLocData(
        83,
        SSLocFlag.GODDESS,
        "Thunderhead",
        "F023",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0xB, 0x04, "Sky"],
    ),
    "Thunderhead - Goddess Chest outside Isle of Songs": SSLocData(
        84,
        SSLocFlag.GODDESS,
        "Thunderhead",
        "F023",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0xB, 0x02, "Sky"],
    ),
    "Thunderhead - First Goddess Chest on Mogma Mitts Island": SSLocData(
        85,
        SSLocFlag.GODDESS,
        "Thunderhead",
        "F023",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0xB, 0x01, "Sky"],
    ),
    "Thunderhead - Second Goddess Chest on Mogma Mitts Island": SSLocData(
        86,
        SSLocFlag.GODDESS,
        "Thunderhead",
        "F023",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0xA, 0x08, "Sky"],
    ),
    "Thunderhead - Bug Heaven Goddess Chest": SSLocData(
        87,
        SSLocFlag.GODDESS,
        "Thunderhead",
        "F023",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0xA, 0x04, "Sky"],
    ),
    # Sealed Grounds
    "Sealed Grounds - Chest inside Sealed Temple": SSLocData(
        88,
        SSLocFlag.ALWAYS,
        "Sealed Grounds",
        "F402",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0xB, 0x80, "Sealed Grounds"],
    ),
    "Sealed Grounds - Song from Impa": SSLocData(
        89,
        SSLocFlag.ALWAYS,
        "Sealed Grounds",
        "F402",
        SSLocType.EVENT,
        [SSLocCheckedFlag.SCENE, 0x2, 0x20, "Sealed Grounds"],
    ),
    "Sealed Grounds - Gorko's Goddess Wall Reward": SSLocData(
        90,
        SSLocFlag.ALWAYS,
        "Sealed Grounds",
        "F400",
        SSLocType.EVENT,
        [SSLocCheckedFlag.SCENE, 0xF, 0x02, "Sealed Grounds"],  # CHECKTHIS
    ),
    "Sealed Grounds - Zelda's Blessing": SSLocData(
        91,
        SSLocFlag.ALWAYS,
        "Sealed Grounds",
        "F404",
        SSLocType.EVENT,
        [SSLocCheckedFlag.STORY, 0x1, 0x08, 0x805A9B00],  # Flag 349
    ),
    # Faron Woods
    "Faron Woods - Item behind Lower Bombable Rock": SSLocData(
        92,
        SSLocFlag.ALWAYS,
        "Faron Woods",
        "F100",
        SSLocType.ITEM,
        [SSLocCheckedFlag.SCENE, 0x5, 0x02, "Faron Woods"],
    ),
    "Faron Woods - Item on Tree": SSLocData(
        93,
        SSLocFlag.ALWAYS,
        "Faron Woods",
        "F100",
        SSLocType.ITEM,
        [SSLocCheckedFlag.SCENE, 0x9, 0x10, "Faron Woods"],
    ),
    "Faron Woods - Kikwi Elder's Reward": SSLocData(
        94,
        SSLocFlag.ALWAYS,
        "Faron Woods",
        "F100",
        SSLocType.EVENT,
        [SSLocCheckedFlag.STORY, 0xC, 0x10, 0x805A9AD0],  # Flag 57
    ),
    "Faron Woods - Rupee on Hollow Tree Root": SSLocData(
        95,
        SSLocFlag.RUPEE,
        "Faron Woods",
        "F100",
        SSLocType.ITEM,
        [SSLocCheckedFlag.SCENE, 0x4, 0x04, "Faron Woods"],
    ),
    "Faron Woods - Rupee on Hollow Tree Branch": SSLocData(
        96,
        SSLocFlag.RUPEE,
        "Faron Woods",
        "F100",
        SSLocType.ITEM,
        [SSLocCheckedFlag.SCENE, 0x4, 0x02, "Faron Woods"],
    ),
    "Faron Woods - Rupee on Platform near Floria Door": SSLocData(
        97,
        SSLocFlag.RUPEE,
        "Faron Woods",
        "F100",
        SSLocType.ITEM,
        [SSLocCheckedFlag.SCENE, 0x4, 0x01, "Faron Woods"],
    ),
    "Faron Woods - Deep Woods Chest": SSLocData(
        98,
        SSLocFlag.ALWAYS,
        "Faron Woods",
        "F101",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0xF, 0x80, "Faron Woods"],
    ),
    "Faron Woods - Chest behind Upper Bombable Rock": SSLocData(
        99,
        SSLocFlag.ALWAYS,
        "Faron Woods",
        "F100",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0xF, 0x40, "Faron Woods"],
    ),
    "Faron Woods - Chest inside Great Tree": SSLocData(
        100,
        SSLocFlag.ALWAYS,
        "Faron Woods",
        "F100_1",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0xF, 0x20, "Faron Woods"],
    ),
    "Faron Woods - Rupee on Great Tree North Branch": SSLocData(
        101,
        SSLocFlag.RUPEE,
        "Faron Woods",
        "F100",
        SSLocType.ITEM,
        [SSLocCheckedFlag.SCENE, 0x4, 0x08, "Faron Woods"],
    ),
    "Faron Woods - Rupee on Great Tree West Branch": SSLocData(
        102,
        SSLocFlag.RUPEE,
        "Faron Woods",
        "F100",
        SSLocType.ITEM,
        [SSLocCheckedFlag.SCENE, 0x4, 0x10, "Faron Woods"],
    ),
    # Lake Floria
    "Lake Floria - Rupee under Central Boulder": SSLocData(
        103,
        SSLocFlag.RUPEE,
        "Lake Floria",
        "F102",
        SSLocType.ITEM,
        [SSLocCheckedFlag.SCENE, 0x6, 0x10, "Lake Floria"],
    ),
    "Lake Floria - Rupee behind Southwest Boulder": SSLocData(
        104,
        SSLocFlag.RUPEE,
        "Lake Floria",
        "F102",
        SSLocType.ITEM,
        [SSLocCheckedFlag.SCENE, 0x6, 0x80, "Lake Floria"],
    ),
    "Lake Floria - Left Rupee behind Northwest Boulder": SSLocData(
        105,
        SSLocFlag.RUPEE,
        "Lake Floria",
        "F102",
        SSLocType.ITEM,
        [SSLocCheckedFlag.SCENE, 0x6, 0x40, "Lake Floria"],
    ),
    "Lake Floria - Right Rupee behind Northwest Boulder": SSLocData(
        106,
        SSLocFlag.RUPEE,
        "Lake Floria",
        "F102",
        SSLocType.ITEM,
        [SSLocCheckedFlag.SCENE, 0x6, 0x20, "Lake Floria"],
    ),
    "Lake Floria - Lake Floria Chest": SSLocData(
        107,
        SSLocFlag.ALWAYS,
        "Lake Floria",
        "F102",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0xF, 0x80, "Lake Floria"],
    ),
    "Lake Floria - Dragon Lair South Chest": SSLocData(
        108,
        SSLocFlag.ALWAYS,
        "Lake Floria",
        "F102_2",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0xF, 0x20, "Lake Floria"],
    ),
    "Lake Floria - Dragon Lair East Chest": SSLocData(
        109,
        SSLocFlag.ALWAYS,
        "Lake Floria",
        "F102_2",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0xF, 0x40, "Lake Floria"],
    ),
    "Lake Floria - Rupee on High Ledge outside Ancient Cistern Entrance": SSLocData(
        110,
        SSLocFlag.RUPEE,
        "Lake Floria",
        "F102_1",
        SSLocType.ITEM,
        [SSLocCheckedFlag.SCENE, 0x9, 0x01, "Lake Floria"],
    ),
    # Flooded Faron Woods
    "Flooded Faron Woods - Yellow Tadtone under Lilypad": SSLocData(
        111,
        SSLocFlag.TADTONE,
        "Flooded Faron Woods",
        "F103",
        SSLocType.CLEF,
        [SSLocCheckedFlag.SCENE, 0x4, 0x01, "Flooded Faron Woods"],
    ),
    "Flooded Faron Woods - 8 Light Blue Tadtones near Viewing Platform": SSLocData(
        112,
        SSLocFlag.TADTONE,
        "Flooded Faron Woods",
        "F103",
        SSLocType.CLEF,
        [SSLocCheckedFlag.SCENE, 0x5, 0x04, "Flooded Faron Woods"],
    ),
    "Flooded Faron Woods - 4 Purple Tadtones under Viewing Platform": SSLocData(
        113,
        SSLocFlag.TADTONE,
        "Flooded Faron Woods",
        "F103",
        SSLocType.CLEF,
        [SSLocCheckedFlag.SCENE, 0x5, 0x01, "Flooded Faron Woods"],
    ),
    "Flooded Faron Woods - Red Moving Tadtone near Viewing Platform": SSLocData(
        114,
        SSLocFlag.TADTONE,
        "Flooded Faron Woods",
        "F103",
        SSLocType.CLEF,
        [SSLocCheckedFlag.SCENE, 0x2, 0x80, "Flooded Faron Woods"],
    ),
    "Flooded Faron Woods - Light Blue Tadtone under Great Tree Root": SSLocData(
        115,
        SSLocFlag.TADTONE,
        "Flooded Faron Woods",
        "F103",
        SSLocType.CLEF,
        [SSLocCheckedFlag.SCENE, 0x4, 0x08, "Flooded Faron Woods"],
    ),
    "Flooded Faron Woods - 8 Yellow Tadtones near Kikwi Elder": SSLocData(
        116,
        SSLocFlag.TADTONE,
        "Flooded Faron Woods",
        "F103",
        SSLocType.CLEF,
        [SSLocCheckedFlag.SCENE, 0x5, 0x10, "Flooded Faron Woods"],
    ),
    "Flooded Faron Woods - 4 Light Blue Moving Tadtones under Kikwi Elder": SSLocData(
        117,
        SSLocFlag.TADTONE,
        "Flooded Faron Woods",
        "F103",
        SSLocType.CLEF,
        [SSLocCheckedFlag.SCENE, 0x5, 0x40, "Flooded Faron Woods"],
    ),
    "Flooded Faron Woods - 4 Red Moving Tadtones North West of Great Tree": SSLocData(
        118,
        SSLocFlag.TADTONE,
        "Flooded Faron Woods",
        "F103",
        SSLocType.CLEF,
        [SSLocCheckedFlag.SCENE, 0x4, 0x02, "Flooded Faron Woods"],
    ),
    "Flooded Faron Woods - Green Tadtone behind Upper Bombable Rock": SSLocData(
        119,
        SSLocFlag.TADTONE,
        "Flooded Faron Woods",
        "F103",
        SSLocType.CLEF,
        [SSLocCheckedFlag.SCENE, 0x5, 0x08, "Flooded Faron Woods"],
    ),
    "Flooded Faron Woods - 2 Dark Blue Tadtones in Grass West of Great Tree": SSLocData(
        120,
        SSLocFlag.TADTONE,
        "Flooded Faron Woods",
        "F103",
        SSLocType.CLEF,
        [SSLocCheckedFlag.SCENE, 0x5, 0x02, "Flooded Faron Woods"],
    ),
    "Flooded Faron Woods - 8 Green Tadtones in West Tunnel": SSLocData(
        121,
        SSLocFlag.TADTONE,
        "Flooded Faron Woods",
        "F103",
        SSLocType.CLEF,
        [SSLocCheckedFlag.SCENE, 0x5, 0x80, "Flooded Faron Woods"],
    ),
    "Flooded Faron Woods - 2 Red Tadtones in Grass near Lower Bombable Rock": SSLocData(
        122,
        SSLocFlag.TADTONE,
        "Flooded Faron Woods",
        "F103",
        SSLocType.CLEF,
        [SSLocCheckedFlag.SCENE, 0x4, 0x20, "Flooded Faron Woods"],
    ),
    "Flooded Faron Woods - 16 Dark Blue Tadtones in the South West": SSLocData(
        123,
        SSLocFlag.TADTONE,
        "Flooded Faron Woods",
        "F103",
        SSLocType.CLEF,
        [SSLocCheckedFlag.SCENE, 0x4, 0x80, "Flooded Faron Woods"],
    ),
    "Flooded Faron Woods - 4 Purple Moving Tadtones near Floria Gate": SSLocData(
        124,
        SSLocFlag.TADTONE,
        "Flooded Faron Woods",
        "F103",
        SSLocType.CLEF,
        [SSLocCheckedFlag.SCENE, 0x4, 0x40, "Flooded Faron Woods"],
    ),
    "Flooded Faron Woods - Dark Blue Moving Tadtone inside Small Hollow Tree": SSLocData(
        125,
        SSLocFlag.TADTONE,
        "Flooded Faron Woods",
        "F103",
        SSLocType.CLEF,
        [SSLocCheckedFlag.SCENE, 0x5, 0x20, "Flooded Faron Woods"],
    ),
    "Flooded Faron Woods - 4 Yellow Tadtones under Small Hollow Tree": SSLocData(
        126,
        SSLocFlag.TADTONE,
        "Flooded Faron Woods",
        "F103",
        SSLocType.CLEF,
        [SSLocCheckedFlag.SCENE, 0x4, 0x10, "Flooded Faron Woods"],
    ),
    "Flooded Faron Woods - 8 Purple Tadtones in Clearing after Small Hollow Tree": SSLocData(
        127,
        SSLocFlag.TADTONE,
        "Flooded Faron Woods",
        "F103",
        SSLocType.CLEF,
        [SSLocCheckedFlag.SCENE, 0x4, 0x04, "Flooded Faron Woods"],
    ),
    "Flooded Faron Woods - Water Dragon's Reward": SSLocData(
        128,
        SSLocFlag.ALWAYS,
        "Flooded Faron Woods",
        "F103_1",
        SSLocType.EVENT,
        [SSLocCheckedFlag.STORY, 0xB, 0x02, 0x805A9AD0],  # Flag 16
    ),
    # Eldin Volcano
    "Eldin Volcano - Rupee on Ledge before First Room": SSLocData(
        129,
        SSLocFlag.RUPEE,
        "Eldin Volcano",
        "F200",
        SSLocType.ITEM,
        [SSLocCheckedFlag.SCENE, 0x4, 0x02, "Eldin Volcano"],
    ),
    "Eldin Volcano - Chest behind Bombable Wall in First Room": SSLocData(
        130,
        SSLocFlag.ALWAYS,
        "Eldin Volcano",
        "F200",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0xE, 0x40, "Eldin Volcano"],
    ),
    "Eldin Volcano - Rupee behind Bombable Wall in First Room": SSLocData(
        131,
        SSLocFlag.RUPEE,
        "Eldin Volcano",
        "F200",
        SSLocType.ITEM,
        [SSLocCheckedFlag.SCENE, 0x0, 0x20, "Eldin Volcano"],
    ),
    "Eldin Volcano - Rupee in Crawlspace in First Room": SSLocData(
        132,
        SSLocFlag.RUPEE,
        "Eldin Volcano",
        "F200",
        SSLocType.ITEM,
        [SSLocCheckedFlag.SCENE, 0x3, 0x08, "Eldin Volcano"],
    ),
    "Eldin Volcano - Chest after Crawlspace": SSLocData(
        133,
        SSLocFlag.ALWAYS,
        "Eldin Volcano",
        "F200",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0xC, 0x40, "Eldin Volcano"],
    ),
    "Eldin Volcano - Southeast Rupee above Mogma Turf Entrance": SSLocData(
        134,
        SSLocFlag.RUPEE,
        "Eldin Volcano",
        "F200",
        SSLocType.ITEM,
        [SSLocCheckedFlag.SCENE, 0xE, 0x20, "Eldin Volcano"],
    ),
    "Eldin Volcano - North Rupee above Mogma Turf Entrance": SSLocData(
        135,
        SSLocFlag.RUPEE,
        "Eldin Volcano",
        "F200",
        SSLocType.ITEM,
        [SSLocCheckedFlag.SCENE, 0xE, 0x08, "Eldin Volcano"],
    ),
    "Eldin Volcano - Chest behind Bombable Wall near Cliff": SSLocData(
        136,
        SSLocFlag.ALWAYS,
        "Eldin Volcano",
        "F200",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0x3, 0x40, "Eldin Volcano"],
    ),
    "Eldin Volcano - Item on Cliff": SSLocData(
        137,
        SSLocFlag.ALWAYS,
        "Eldin Volcano",
        "F200",
        SSLocType.ITEM,
        [SSLocCheckedFlag.SCENE, 0xD, 0x40, "Eldin Volcano"],
    ),
    "Eldin Volcano - Chest behind Bombable Wall near Volcano Ascent": SSLocData(
        138,
        SSLocFlag.ALWAYS,
        "Eldin Volcano",
        "F200",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0x9, 0x10, "Eldin Volcano"],
    ),
    "Eldin Volcano - Left Rupee behind Bombable Wall on First Slope": SSLocData(
        139,
        SSLocFlag.RUPEE,
        "Eldin Volcano",
        "F200",
        SSLocType.ITEM,
        [SSLocCheckedFlag.SCENE, 0x4, 0x20, "Eldin Volcano"],
    ),
    "Eldin Volcano - Right Rupee behind Bombable Wall on First Slope": SSLocData(
        140,
        SSLocFlag.RUPEE,
        "Eldin Volcano",
        "F200",
        SSLocType.ITEM,
        [SSLocCheckedFlag.SCENE, 0x0, 0x08, "Eldin Volcano"],
    ),
    "Eldin Volcano - Digging Spot in front of Earth Temple": SSLocData(
        141,
        SSLocFlag.ALWAYS,
        "Eldin Volcano",
        "F200",
        SSLocType.SOIL,
        [SSLocCheckedFlag.SCENE, 0x0, 0x01, "Eldin Volcano"],
    ),
    "Eldin Volcano - Digging Spot below Tower": SSLocData(
        142,
        SSLocFlag.ALWAYS,
        "Eldin Volcano",
        "F200",
        SSLocType.SOIL,
        [SSLocCheckedFlag.SCENE, 0x0, 0x02, "Eldin Volcano"],
    ),
    "Eldin Volcano - Digging Spot behind Boulder on Sandy Slope": SSLocData(
        143,
        SSLocFlag.ALWAYS,
        "Eldin Volcano",
        "F200",
        SSLocType.SOIL,
        [SSLocCheckedFlag.SCENE, 0x0, 0x10, "Eldin Volcano"],
    ),
    "Eldin Volcano - Digging Spot after Vents": SSLocData(
        144,
        SSLocFlag.ALWAYS,
        "Eldin Volcano",
        "F200",
        SSLocType.SOIL,
        [SSLocCheckedFlag.SCENE, 0x0, 0x04, "Eldin Volcano"],
    ),
    "Eldin Volcano - Digging Spot after Draining Lava": SSLocData(
        145,
        SSLocFlag.ALWAYS,
        "Eldin Volcano",
        "F200",
        SSLocType.SOIL,
        [SSLocCheckedFlag.SCENE, 0x9, 0x01, "Eldin Volcano"],
    ),
    # Mogma Turf
    "Mogma Turf - Free Fall Chest": SSLocData(
        146,
        SSLocFlag.ALWAYS,
        "Mogma Turf",
        "F210",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0xC, 0x10, "Eldin Volcano"],
    ),
    "Mogma Turf - Chest behind Bombable Wall at Entrance": SSLocData(
        147,
        SSLocFlag.ALWAYS,
        "Mogma Turf",
        "F210",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0xF, 0x04, "Eldin Volcano"],
    ),
    "Mogma Turf - Defeat Bokoblins": SSLocData(
        148,
        SSLocFlag.ALWAYS,
        "Mogma Turf",
        "F210",
        SSLocType.EVENT,
        [SSLocCheckedFlag.SCENE, 0x1, 0x08, "Eldin Volcano"],
    ),
    "Mogma Turf - Sand Slide Chest": SSLocData(
        149,
        SSLocFlag.ALWAYS,
        "Mogma Turf",
        "F210",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0xF, 0x02, "Eldin Volcano"],
    ),
    "Mogma Turf - Chest behind Bombable Wall in Fire Maze": SSLocData(
        150,
        SSLocFlag.ALWAYS,
        "Mogma Turf",
        "F210",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0x4, 0x01, "Eldin Volcano"],
    ),
    # Volcano Summit
    "Volcano Summit - Chest behind Bombable Wall in Waterfall Area": SSLocData(
        151,
        SSLocFlag.ALWAYS,
        "Volcano Summit",
        "F201_4",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0xC, 0x01, "Boko Base/Volcano Summit"],
    ),
    "Volcano Summit - Item behind Digging": SSLocData(
        152,
        SSLocFlag.ALWAYS,
        "Volcano Summit",
        "F201_3",
        SSLocType.ITEM,
        [SSLocCheckedFlag.SCENE, 0xE, 0x80, "Boko Base/Volcano Summit"],
    ),
    # Bokoblin Base
    "Bokoblin Base - Plats' Gift": SSLocData(
        153,
        SSLocFlag.ALWAYS,
        "Bokoblin Base",
        "F202",
        SSLocType.EVENT,
        [SSLocCheckedFlag.STORY, 0x5, 0x01, 0x805A9AE0],  # Flag 177
    ),
    "Bokoblin Base - Chest near Bone Bridge": SSLocData(
        154,
        SSLocFlag.ALWAYS,
        "Bokoblin Base",
        "F202",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0x8, 0x08, "Boko Base/Volcano Summit"],
    ),
    "Bokoblin Base - Chest on Cliff": SSLocData(
        155,
        SSLocFlag.ALWAYS,
        "Bokoblin Base",
        "F202",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0x8, 0x10, "Boko Base/Volcano Summit"],
    ),
    "Bokoblin Base - Chest near Drawbridge": SSLocData(
        156,
        SSLocFlag.ALWAYS,
        "Bokoblin Base",
        "F202",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0x8, 0x20, "Boko Base/Volcano Summit"],
    ),
    "Bokoblin Base - Chest East of Earth Temple Entrance": SSLocData(
        157,
        SSLocFlag.ALWAYS,
        "Bokoblin Base",
        "F202",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0x8, 0x40, "Boko Base/Volcano Summit"],
    ),
    "Bokoblin Base - Chest West of Earth Temple Entrance": SSLocData(
        158,
        SSLocFlag.ALWAYS,
        "Bokoblin Base",
        "F202",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0x8, 0x80, "Boko Base/Volcano Summit"],
    ),
    "Bokoblin Base - First Chest in Volcano Summit": SSLocData(
        159,
        SSLocFlag.ALWAYS,
        "Bokoblin Base",
        "F201_2",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0x7, 0x40, "Boko Base/Volcano Summit"],
    ),
    "Bokoblin Base - Raised Chest in Volcano Summit": SSLocData(
        160,
        SSLocFlag.ALWAYS,
        "Bokoblin Base",
        "F201_2",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0x7, 0x80, "Boko Base/Volcano Summit"],
    ),
    "Bokoblin Base - Chest in Volcano Summit Alcove": SSLocData(
        161,
        SSLocFlag.ALWAYS,
        "Bokoblin Base",
        "F201_2",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0x6, 0x40, "Boko Base/Volcano Summit"],
    ),
    "Bokoblin Base - Fire Dragon's Reward": SSLocData(
        162,
        SSLocFlag.ALWAYS,
        "Bokoblin Base",
        "F221",
        SSLocType.EVENT,
        [SSLocCheckedFlag.STORY, 0xB, 0x08, 0x805A9AD0],  # Flag 19
    ),
    # Lanayru Mine
    "Lanayru Mine - Chest behind First Landing": SSLocData(
        163,
        SSLocFlag.ALWAYS,
        "Lanayru Mine",
        "F300_1",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0x4, 0x80, "Lanayru Desert"],
    ),
    "Lanayru Mine - Chest near First Timeshift Stone": SSLocData(
        164,
        SSLocFlag.ALWAYS,
        "Lanayru Mine",
        "F300_1",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0x4, 0x40, "Lanayru Desert"],
    ),
    "Lanayru Mine - Chest behind Statue": SSLocData(
        165,
        SSLocFlag.ALWAYS,
        "Lanayru Mine",
        "F300_1",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0x4, 0x20, "Lanayru Desert"],
    ),
    "Lanayru Mine - Chest at the End of Mine": SSLocData(
        166,
        SSLocFlag.ALWAYS,
        "Lanayru Mine",
        "F300_1",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0x4, 0x10, "Lanayru Desert"],
    ),
    # Lanayru Desert
    "Lanayru Desert - Chest near Party Wheel": SSLocData(
        167,
        SSLocFlag.ALWAYS,
        "Lanayru Desert",
        "F300",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0x4, 0x08, "Lanayru Desert"],
    ),
    "Lanayru Desert - Chest near Caged Robot": SSLocData(
        168,
        SSLocFlag.ALWAYS,
        "Lanayru Desert",
        "F300",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0xF, 0x01, "Lanayru Desert"],
    ),
    "Lanayru Desert - Rescue Caged Robot": SSLocData(
        169,
        SSLocFlag.ALWAYS,
        "Lanayru Desert",
        "F300",
        SSLocType.EVENT,
        [SSLocCheckedFlag.STORY, 0xF, 0x80, 0x805A9AE0],  # Flag 90
    ),
    "Lanayru Desert - Chest on Platform near Fire Node": SSLocData(
        170,
        SSLocFlag.ALWAYS,
        "Lanayru Desert",
        "F300",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0x4, 0x04, "Lanayru Desert"],
    ),
    "Lanayru Desert - Chest on Platform near Lightning Node": SSLocData(
        171,
        SSLocFlag.ALWAYS,
        "Lanayru Desert",
        "F300",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0x4, 0x02, "Lanayru Desert"],
    ),
    "Lanayru Desert - Chest near Sand Oasis": SSLocData(
        172,
        SSLocFlag.ALWAYS,
        "Lanayru Desert",
        "F300",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0x8, 0x01, "Lanayru Desert"],
    ),
    "Lanayru Desert - Chest on top of Lanayru Mining Facility": SSLocData(
        173,
        SSLocFlag.ALWAYS,
        "Lanayru Desert",
        "F300",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0x7, 0x01, "Lanayru Desert"],
    ),
    "Lanayru Desert - Secret Passageway Chest": SSLocData(
        174,
        SSLocFlag.ALWAYS,
        "Lanayru Desert",
        "F300",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0x7, 0x40, "Lanayru Desert"],  # CHECKTHIS
    ),
    "Lanayru Desert - Fire Node - Shortcut Chest": SSLocData(
        175,
        SSLocFlag.ALWAYS,
        "Lanayru Desert",
        "F300_3",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0xB, 0x04, "Lanayru Desert"],
    ),
    "Lanayru Desert - Fire Node - First Small Chest": SSLocData(
        176,
        SSLocFlag.ALWAYS,
        "Lanayru Desert",
        "F300_3",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0xB, 0x08, "Lanayru Desert"],
    ),
    "Lanayru Desert - Fire Node - Second Small Chest": SSLocData(
        177,
        SSLocFlag.ALWAYS,
        "Lanayru Desert",
        "F300_3",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0xC, 0x40, "Lanayru Desert"],
    ),
    "Lanayru Desert - Fire Node - Left Ending Chest": SSLocData(
        178,
        SSLocFlag.ALWAYS,
        "Lanayru Desert",
        "F300_3",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0xE, 0x20, "Lanayru Desert"],
    ),
    "Lanayru Desert - Fire Node - Right Ending Chest": SSLocData(
        179,
        SSLocFlag.ALWAYS,
        "Lanayru Desert",
        "F300",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0xE, 0x80, "Lanayru Desert"],  # CHECKTHIS
    ),
    "Lanayru Desert - Lightning Node - First Chest": SSLocData(
        180,
        SSLocFlag.ALWAYS,
        "Lanayru Desert",
        "F300_2",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0xC, 0x08, "Lanayru Desert"],  # CHECKTHIS
    ),
    "Lanayru Desert - Lightning Node - Second Chest": SSLocData(
        181,
        SSLocFlag.ALWAYS,
        "Lanayru Desert",
        "F300_2",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0xB, 0x20, "Lanayru Desert"],  # CHECKTHIS
    ),
    "Lanayru Desert - Lightning Node - Raised Chest near Generator": SSLocData(
        182,
        SSLocFlag.ALWAYS,
        "Lanayru Desert",
        "F300_2",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0xB, 0x40, "Lanayru Desert"],  # CHECKTHIS
    ),
    # Lanayru Caves
    "Lanayru Caves - Chest": SSLocData(
        183,
        SSLocFlag.ALWAYS,
        "Lanayru Caves",
        "F303",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0xB, 0x40, "Lanayru Gorge"],
    ),
    "Lanayru Caves - Golo's Gift": SSLocData(
        184,
        SSLocFlag.ALWAYS,
        "Lanayru Caves",
        "F303",
        SSLocType.EVENT,
        [SSLocCheckedFlag.SCENE, 0xC, 0x10, "Lanayru Gorge"],  # CHECKTHIS
    ),
    # Lanayru Gorge
    "Lanayru Gorge - Thunder Dragon's Reward": SSLocData(
        185,
        SSLocFlag.ALWAYS,
        "Lanayru Gorge",
        "F302",
        SSLocType.EVENT,
        [SSLocCheckedFlag.STORY, 0xB, 0x20, 0x805A9AD0],  # Flag 21
    ),
    "Lanayru Gorge - Item on Pillar": SSLocData(
        186,
        SSLocFlag.ALWAYS,
        "Lanayru Gorge",
        "F302",
        SSLocType.ITEM,
        [SSLocCheckedFlag.SCENE, 0x0, 0x02, "Lanayru Gorge"],
    ),
    "Lanayru Gorge - Digging Spot": SSLocData(
        187,
        SSLocFlag.ALWAYS,
        "Lanayru Gorge",
        "F302",
        SSLocType.SOIL,
        [SSLocCheckedFlag.SCENE, 0x2, 0x40, "Lanayru Gorge"],  # CHECKTHIS
    ),
    # Lanayru Sand Sea
    "Lanayru Sand Sea - Ancient Harbour - Rupee on First Pillar": SSLocData(
        188,
        SSLocFlag.RUPEE,
        "Lanayru Sand Sea",
        "F301",
        SSLocType.ITEM,
        [SSLocCheckedFlag.SCENE, 0xA, 0x10, "Lanayru Sand Sea"],
    ),
    "Lanayru Sand Sea - Ancient Harbour - Left Rupee on Entrance Crown": SSLocData(
        189,
        SSLocFlag.RUPEE,
        "Lanayru Sand Sea",
        "F301",
        SSLocType.ITEM,
        [SSLocCheckedFlag.SCENE, 0xA, 0x08, "Lanayru Sand Sea"],
    ),
    "Lanayru Sand Sea - Ancient Harbour - Right Rupee on Entrance Crown": SSLocData(
        190,
        SSLocFlag.RUPEE,
        "Lanayru Sand Sea",
        "F301",
        SSLocType.ITEM,
        [SSLocCheckedFlag.SCENE, 0xA, 0x20, "Lanayru Sand Sea"],
    ),
    "Lanayru Sand Sea - Skipper's Retreat - Chest after Moblin": SSLocData(
        191,
        SSLocFlag.ALWAYS,
        "Lanayru Sand Sea",
        "F301_3",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0xF, 0x80, "Lanayru Sand Sea"],
    ),
    "Lanayru Sand Sea - Skipper's Retreat - Chest on top of Cacti Pillar": SSLocData(
        192,
        SSLocFlag.ALWAYS,
        "Lanayru Sand Sea",
        "F301_3",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0xF, 0x40, "Lanayru Sand Sea"],
    ),
    "Lanayru Sand Sea - Skipper's Retreat - Chest in Shack": SSLocData(
        193,
        SSLocFlag.ALWAYS,
        "Lanayru Sand Sea",
        "F301_5",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0x3, 0x02, "Lanayru Sand Sea"],
    ),
    "Lanayru Sand Sea - Skipper's Retreat - Skydive Chest": SSLocData(
        194,
        SSLocFlag.ALWAYS,
        "Lanayru Sand Sea",
        "F301_3",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0xF, 0x20, "Lanayru Sand Sea"],
    ),
    "Lanayru Sand Sea - Rickety Coaster -- Heart Stopping Track in 1'05": SSLocData(
        195,
        SSLocFlag.MINIGME,
        "Lanayru Sand Sea",
        "F301_4",
        SSLocType.EVENT,
        [SSLocCheckedFlag.STORY, 0xE, 0x02, 0x805A9B10],  # Flag 667
    ),
    "Lanayru Sand Sea - Pirate Stronghold - Rupee on East Sea Pillar": SSLocData(
        196,
        SSLocFlag.RUPEE,
        "Lanayru Sand Sea",
        "F301_6",
        SSLocType.ITEM,
        [SSLocCheckedFlag.SCENE, 0x0, 0x10, "Lanayru Sand Sea"],
    ),
    "Lanayru Sand Sea - Pirate Stronghold - Rupee on West Sea Pillar": SSLocData(
        197,
        SSLocFlag.RUPEE,
        "Lanayru Sand Sea",
        "F301_6",
        SSLocType.ITEM,
        [SSLocCheckedFlag.SCENE, 0x0, 0x08, "Lanayru Sand Sea"],
    ),
    "Lanayru Sand Sea - Pirate Stronghold - Rupee on Bird Statue Pillar or Nose": SSLocData(
        198,
        SSLocFlag.RUPEE,
        "Lanayru Sand Sea",
        "F301_6",
        SSLocType.ITEM,
        [SSLocCheckedFlag.SCENE, 0x0, 0x20, "Lanayru Sand Sea"],
    ),
    "Lanayru Sand Sea - Pirate Stronghold - First Chest": SSLocData(
        199,
        SSLocFlag.ALWAYS,
        "Lanayru Sand Sea",
        "F301_2",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0xF, 0x10, "Lanayru Sand Sea"],
    ),
    "Lanayru Sand Sea - Pirate Stronghold - Second Chest": SSLocData(
        200,
        SSLocFlag.ALWAYS,
        "Lanayru Sand Sea",
        "F301_2",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0xF, 0x08, "Lanayru Sand Sea"],
    ),
    "Lanayru Sand Sea - Pirate Stronghold - Third Chest": SSLocData(
        201,
        SSLocFlag.ALWAYS,
        "Lanayru Sand Sea",
        "F301_2",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0xF, 0x04, "Lanayru Sand Sea"],
    ),
    # Skyview (SV)
    "Skyview - Chest on Tree Branch": SSLocData(
        202,
        SSLocFlag.D_SV,
        "Skyview",
        "D100",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0x0, 0x08, "Skyview"],
    ),
    "Skyview - Digging Spot in Crawlspace": SSLocData(
        203,
        SSLocFlag.D_SV,
        "Skyview",
        "D100",
        SSLocType.SOIL,
        [SSLocCheckedFlag.SCENE, 0x0, 0x80, "Skyview"],
    ),
    "Skyview - Chest behind Two Eyes": SSLocData(
        204,
        SSLocFlag.D_SV,
        "Skyview",
        "D100",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0xF, 0x20, "Skyview"],
    ),
    "Skyview - Chest after Stalfos Fight": SSLocData(
        205,
        SSLocFlag.D_SV,
        "Skyview",
        "D100",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0x5, 0x02, "Skyview"],  # CHECKTHIS
    ),
    "Skyview - Item behind Bars": SSLocData(
        206,
        SSLocFlag.D_SV,
        "Skyview",
        "D100",
        SSLocType.ITEM,
        [SSLocCheckedFlag.SCENE, 0xD, 0x80, "Skyview"],
    ),
    "Skyview - Rupee in Southeast Tunnel": SSLocData(
        207,
        SSLocFlag.D_SV | SSLocFlag.RUPEE,
        "Skyview",
        "D100",
        SSLocType.ITEM,
        [SSLocCheckedFlag.SCENE, 0x9, 0x02, "Skyview"],
    ),
    "Skyview - Rupee in Southwest Tunnel": SSLocData(
        208,
        SSLocFlag.D_SV | SSLocFlag.RUPEE,
        "Skyview",
        "D100",
        SSLocType.ITEM,
        [SSLocCheckedFlag.SCENE, 0x9, 0x08, "Skyview"],
    ),
    "Skyview - Rupee in East Tunnel": SSLocData(
        209,
        SSLocFlag.D_SV | SSLocFlag.RUPEE,
        "Skyview",
        "D100",
        SSLocType.ITEM,
        [SSLocCheckedFlag.SCENE, 0x9, 0x04, "Skyview"],
    ),
    "Skyview - Chest behind Three Eyes": SSLocData(
        210,
        SSLocFlag.D_SV,
        "Skyview",
        "D100",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0xF, 0x40, "Skyview"],
    ),
    "Skyview - Chest near Boss Door": SSLocData(
        211,
        SSLocFlag.D_SV,
        "Skyview",
        "D100",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0xB, 0x10, "Skyview"],  # CHECKTHIS
    ),
    "Skyview - Boss Key Chest": SSLocData(
        212,
        SSLocFlag.D_SV,
        "Skyview",
        "D100",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0x2, 0x40, "Skyview"],
    ),
    "Skyview - Heart Container": SSLocData(
        213,
        SSLocFlag.D_SV,
        "Skyview",
        "B100",
        SSLocType.HRTCO,
        [SSLocCheckedFlag.SCENE, 0xD, 0x40, "Skyview"],  # CHECKTHIS
    ),
    "Skyview - Rupee on Spring Pillar": SSLocData(
        214,
        SSLocFlag.D_SV | SSLocFlag.RUPEE,
        "Skyview",
        "B100_1",
        SSLocType.ITEM,
        [SSLocCheckedFlag.SCENE, 0xC, 0x20, "Skyview"],
    ),
    "Skyview - Strike Crest": SSLocData(
        215,
        SSLocFlag.D_SV,
        "Skyview",
        "B100_1",
        SSLocType.EVENT,
        [SSLocCheckedFlag.SCENE, 0xC, 0x02, "Skyview"],  # CHECKTHIS
    ),
    # Earth Temple (ET)
    "Earth Temple - Vent Chest": SSLocData(
        216,
        SSLocFlag.D_ET,
        "Earth Temple",
        "D200",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0x6, 0x80, "Earth Temple"],
    ),
    "Earth Temple - Rupee above Drawbridge": SSLocData(
        217,
        SSLocFlag.D_ET | SSLocFlag.RUPEE,
        "Earth Temple",
        "D200",
        SSLocType.ITEM,
        [SSLocCheckedFlag.SCENE, 0x2, 0x02, "Earth Temple"],
    ),
    "Earth Temple - Chest behind Bombable Rock": SSLocData(
        218,
        SSLocFlag.D_ET,
        "Earth Temple",
        "D200",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0x6, 0x40, "Earth Temple"],
    ),
    "Earth Temple - Chest Left of Main Room Bridge": SSLocData(
        219,
        SSLocFlag.D_ET,
        "Earth Temple",
        "D200",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0x6, 0x20, "Earth Temple"],
    ),
    "Earth Temple - Chest in West Room": SSLocData(
        220,
        SSLocFlag.D_ET,
        "Earth Temple",
        "D200",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0x3, 0x02, "Earth Temple"],
    ),
    "Earth Temple - Chest after Double Lizalfos Fight": SSLocData(
        221,
        SSLocFlag.D_ET,
        "Earth Temple",
        "D200",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0x0, 0x02, "Earth Temple"],
    ),
    "Earth Temple - Ledd's Gift": SSLocData(
        222,
        SSLocFlag.D_ET,
        "Earth Temple",
        "D200",
        SSLocType.EVENT,
        [SSLocCheckedFlag.SCENE, 0x4, 0x20, "Earth Temple"],
    ),
    "Earth Temple - Rupee in Lava Tunnel": SSLocData(
        223,
        SSLocFlag.D_ET | SSLocFlag.RUPEE,
        "Earth Temple",
        "D200",
        SSLocType.ITEM,
        [SSLocCheckedFlag.SCENE, 0x3, 0x20, "Earth Temple"],
    ),
    "Earth Temple - Chest Guarded by Lizalfos": SSLocData(
        224,
        SSLocFlag.D_ET,
        "Earth Temple",
        "D200",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0x6, 0x10, "Earth Temple"],
    ),
    "Earth Temple - Boss Key Chest": SSLocData(
        225,
        SSLocFlag.D_ET,
        "Earth Temple",
        "D200",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0x3, 0x80, "Earth Temple"],
    ),
    "Earth Temple - Heart Container": SSLocData(
        226,
        SSLocFlag.D_ET,
        "Earth Temple",
        "B200",
        SSLocType.HRTCO,
        [SSLocCheckedFlag.SCENE, 0x6, 0x01, "Earth Temple"],
    ),
    "Earth Temple - Strike Crest": SSLocData(
        227,
        SSLocFlag.D_ET,
        "Earth Temple",
        "B210",
        SSLocType.EVENT,
        [SSLocCheckedFlag.SCENE, 0x5, 0x40, "Earth Temple"],  # CHECKTHIS
    ),
    # Lanayru Mining Facility (LMF)
    "Lanayru Mining Facility - Chest behind Bars": SSLocData(
        228,
        SSLocFlag.D_LMF,
        "Lanayru Mining Facility",
        "D300",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0x4, 0x20, "Lanayru Mining Facility"],
    ),
    "Lanayru Mining Facility - First Chest in Hub Room": SSLocData(
        229,
        SSLocFlag.D_LMF,
        "Lanayru Mining Facility",
        "D300_1",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0x6, 0x20, "Lanayru Mining Facility"],
    ),
    "Lanayru Mining Facility - Chest in First West Room": SSLocData(
        230,
        SSLocFlag.D_LMF,
        "Lanayru Mining Facility",
        "D300",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0x4, 0x04, "Lanayru Mining Facility"],
    ),
    "Lanayru Mining Facility - Chest after Armos Fight": SSLocData(
        231,
        SSLocFlag.D_LMF,
        "Lanayru Mining Facility",
        "D300",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0x3, 0x40, "Lanayru Mining Facility"],
    ),
    "Lanayru Mining Facility - Chest in Key Locked Room": SSLocData(
        232,
        SSLocFlag.D_LMF,
        "Lanayru Mining Facility",
        "D300",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0x4, 0x02, "Lanayru Mining Facility"],
    ),
    "Lanayru Mining Facility - Raised Chest in Hop across Boxes Room": SSLocData(
        233,
        SSLocFlag.D_LMF,
        "Lanayru Mining Facility",
        "D300",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0x6, 0x02, "Lanayru Mining Facility"],
    ),
    "Lanayru Mining Facility - Lower Chest in Hop across Boxes Room": SSLocData(
        234,
        SSLocFlag.D_LMF,
        "Lanayru Mining Facility",
        "D300",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0x7, 0x02, "Lanayru Mining Facility"],
    ),
    "Lanayru Mining Facility - Chest behind First Crawlspace": SSLocData(
        235,
        SSLocFlag.D_LMF,
        "Lanayru Mining Facility",
        "D300_1",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0x7, 0x80, "Lanayru Mining Facility"],
    ),
    "Lanayru Mining Facility - Chest in Spike Maze": SSLocData(
        236,
        SSLocFlag.D_LMF,
        "Lanayru Mining Facility",
        "D300_1",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0x7, 0x10, "Lanayru Mining Facility"],
    ),
    "Lanayru Mining Facility - Boss Key Chest": SSLocData(
        237,
        SSLocFlag.D_LMF,
        "Lanayru Mining Facility",
        "D300_1",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0x1, 0x40, "Lanayru Mining Facility"],
    ),
    "Lanayru Mining Facility - Shortcut Chest in Main Hub": SSLocData(
        238,
        SSLocFlag.D_LMF,
        "Lanayru Mining Facility",
        "D300_1",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0x7, 0x01, "Lanayru Mining Facility"],
    ),
    "Lanayru Mining Facility - Heart Container": SSLocData(
        239,
        SSLocFlag.D_LMF,
        "Lanayru Mining Facility",
        "B300",
        SSLocType.HRTCO,
        [SSLocCheckedFlag.SCENE, 0xE, 0x40, "Lanayru Mining Facility"],
    ),
    "Lanayru Mining Facility - Exit Hall of Ancient Robots": SSLocData(
        240,
        SSLocFlag.D_LMF,
        "Lanayru Mining Facility",
        "F300_5",
        SSLocType.EVENT,
        [SSLocCheckedFlag.STORY, 0xE, 0x40, 0x805A9B30],  # Flag 936
    ),
    # Ancient Cistern (AC)
    "Ancient Cistern - Rupee in West Hand": SSLocData(
        241,
        SSLocFlag.D_AC | SSLocFlag.RUPEE,
        "Ancient Cistern",
        "D101",
        SSLocType.ITEM,
        [SSLocCheckedFlag.SCENE, 0xA, 0x20, "Ancient Cistern"],
    ),
    "Ancient Cistern - Rupee in East Hand": SSLocData(
        242,
        SSLocFlag.D_AC | SSLocFlag.RUPEE,
        "Ancient Cistern",
        "D101",
        SSLocType.ITEM,
        [SSLocCheckedFlag.SCENE, 0xA, 0x10, "Ancient Cistern"],
    ),
    "Ancient Cistern - First Rupee in East Part in Short Tunnel": SSLocData(
        243,
        SSLocFlag.D_AC | SSLocFlag.RUPEE,
        "Ancient Cistern",
        "D101",
        SSLocType.ITEM,
        [SSLocCheckedFlag.SCENE, 0x9, 0x02, "Ancient Cistern"],
    ),
    "Ancient Cistern - Second Rupee in East Part in Short Tunnel": SSLocData(
        244,
        SSLocFlag.D_AC | SSLocFlag.RUPEE,
        "Ancient Cistern",
        "D101",
        SSLocType.ITEM,
        [SSLocCheckedFlag.SCENE, 0x9, 0x04, "Ancient Cistern"],
    ),
    "Ancient Cistern - Third Rupee in East Part in Short Tunnel": SSLocData(
        245,
        SSLocFlag.D_AC | SSLocFlag.RUPEE,
        "Ancient Cistern",
        "D101",
        SSLocType.ITEM,
        [SSLocCheckedFlag.SCENE, 0x9, 0x08, "Ancient Cistern"],
    ),
    "Ancient Cistern - Rupee in East Part in Cubby": SSLocData(
        246,
        SSLocFlag.D_AC | SSLocFlag.RUPEE,
        "Ancient Cistern",
        "D101",
        SSLocType.ITEM,
        [SSLocCheckedFlag.SCENE, 0x9, 0x10, "Ancient Cistern"],
    ),
    "Ancient Cistern - Rupee in East Part in Main Tunnel": SSLocData(
        247,
        SSLocFlag.D_AC | SSLocFlag.RUPEE,
        "Ancient Cistern",
        "D101",
        SSLocType.ITEM,
        [SSLocCheckedFlag.SCENE, 0x5, 0x04, "Ancient Cistern"],
    ),
    "Ancient Cistern - Chest in East Part": SSLocData(
        248,
        SSLocFlag.D_AC,
        "Ancient Cistern",
        "D101",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0xD, 0x04, "Ancient Cistern"],
    ),
    "Ancient Cistern - Chest after Whip Hooks": SSLocData(
        249,
        SSLocFlag.D_AC,
        "Ancient Cistern",
        "D101",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0x0, 0x08, "Ancient Cistern"],
    ),
    "Ancient Cistern - Chest near Vines": SSLocData(
        250,
        SSLocFlag.D_AC,
        "Ancient Cistern",
        "D101",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0xD, 0x02, "Ancient Cistern"],
    ),
    "Ancient Cistern - Chest behind the Waterfall": SSLocData(
        251,
        SSLocFlag.D_AC,
        "Ancient Cistern",
        "D101",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0xE, 0x01, "Ancient Cistern"],
    ),
    "Ancient Cistern - Bokoblin": SSLocData(
        252,
        SSLocFlag.D_AC,
        "Ancient Cistern",
        "D101",
        SSLocType.EBC,
        [SSLocCheckedFlag.SCENE, 0x9, 0x20, "Ancient Cistern"],  # CHECKTHIS
    ),
    "Ancient Cistern - Rupee under Lilypad": SSLocData(
        253,
        SSLocFlag.D_AC | SSLocFlag.RUPEE,
        "Ancient Cistern",
        "D101",
        SSLocType.ITEM,
        [SSLocCheckedFlag.SCENE, 0x0, 0x20, "Ancient Cistern"],
    ),
    "Ancient Cistern - Chest in Key Locked Room": SSLocData(
        254,
        SSLocFlag.D_AC,
        "Ancient Cistern",
        "D101",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0xC, 0x01, "Ancient Cistern"],
    ),
    "Ancient Cistern - Boss Key Chest": SSLocData(
        255,
        SSLocFlag.D_AC,
        "Ancient Cistern",
        "D101",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0xD, 0x20, "Ancient Cistern"],
    ),
    "Ancient Cistern - Heart Container": SSLocData(
        256,
        SSLocFlag.D_AC,
        "Ancient Cistern",
        "B101",
        SSLocType.HRTCO,
        [SSLocCheckedFlag.SCENE, 0x8, 0x20, "Ancient Cistern"],
    ),
    "Ancient Cistern - Farore's Flame": SSLocData(
        257,
        SSLocFlag.D_AC,
        "Ancient Cistern",
        "B101_1",
        SSLocType.EVENT,
        [SSLocCheckedFlag.SCENE, 0xB, 0x20, "Ancient Cistern"],  # CHECKTHIS
    ),
    # Sandship (SSH)
    "Sandship - Chest at the Stern": SSLocData(
        258,
        SSLocFlag.D_SSH,
        "Sandship",
        "D301",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0x3, 0x20, "Sandship"],
    ),
    "Sandship - Chest before 4-Door Corridor": SSLocData(
        259,
        SSLocFlag.D_SSH,
        "Sandship",
        "D301",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0xE, 0x80, "Sandship"],
    ),
    "Sandship - Chest behind Combination Lock": SSLocData(
        260,
        SSLocFlag.D_SSH,
        "Sandship",
        "D301",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0xE, 0x40, "Sandship"],
    ),
    "Sandship - Treasure Room First Chest": SSLocData(
        261,
        SSLocFlag.D_SSH,
        "Sandship",
        "D301",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0xF, 0x20, "Sandship"],
    ),
    "Sandship - Treasure Room Second Chest": SSLocData(
        262,
        SSLocFlag.D_SSH,
        "Sandship",
        "D301",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0xF, 0x04, "Sandship"],
    ),
    "Sandship - Treasure Room Third Chest": SSLocData(
        263,
        SSLocFlag.D_SSH,
        "Sandship",
        "D301",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0xF, 0x08, "Sandship"],
    ),
    "Sandship - Treasure Room Fourth Chest": SSLocData(
        264,
        SSLocFlag.D_SSH,
        "Sandship",
        "D301",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0xF, 0x10, "Sandship"],
    ),
    "Sandship - Treasure Room Fifth Chest": SSLocData(
        265,
        SSLocFlag.D_SSH,
        "Sandship",
        "D301",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0xF, 0x40, "Sandship"],
    ),
    "Sandship - Robot in Brig's Reward": SSLocData(
        266,
        SSLocFlag.D_SSH,
        "Sandship",
        "D301",
        SSLocType.EVENT,
        [SSLocCheckedFlag.SCENE, 0xC, 0x10, "Sandship"],
    ),
    "Sandship - Chest after Scervo Fight": SSLocData(
        267,
        SSLocFlag.D_SSH,
        "Sandship",
        "D301",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0xA, 0x10, "Sandship"],
    ),
    "Sandship - Boss Key Chest": SSLocData(
        268,
        SSLocFlag.D_SSH,
        "Sandship",
        "D301",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0x3, 0x04, "Sandship"],
    ),
    "Sandship - Heart Container": SSLocData(
        269,
        SSLocFlag.D_SSH,
        "Sandship",
        "B301",
        SSLocType.HRTCO,
        [SSLocCheckedFlag.SCENE, 0xB, 0x20, "Sandship"],
    ),
    "Sandship - Nayru's Flame": SSLocData(
        270,
        SSLocFlag.D_SSH,
        "Sandship",
        "B301",
        SSLocType.EVENT,
        [SSLocCheckedFlag.SCENE, 0xB, 0x80, "Sandship"],  # CHECKTHIS
    ),
    # Fire Sanctuary (FS)
    "Fire Sanctuary - Chest in First Room": SSLocData(
        271,
        SSLocFlag.D_FS,
        "Fire Sanctuary",
        "D201",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0x1, 0x20, "Fire Sanctuary"],
    ),
    "Fire Sanctuary - Chest in Second Room": SSLocData(
        272,
        SSLocFlag.D_FS,
        "Fire Sanctuary",
        "D201_1",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0xF, 0x02, "Fire Sanctuary"],
    ),
    "Fire Sanctuary - Chest on Balcony": SSLocData(
        273,
        SSLocFlag.D_FS,
        "Fire Sanctuary",
        "D201_1",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0xE, 0x40, "Fire Sanctuary"],
    ),
    "Fire Sanctuary - Chest near First Trapped Mogma": SSLocData(
        274,
        SSLocFlag.D_FS,
        "Fire Sanctuary",
        "D201_1",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0xE, 0x08, "Fire Sanctuary"],
    ),
    "Fire Sanctuary - First Chest in Water Fruit Room": SSLocData(
        275,
        SSLocFlag.D_FS,
        "Fire Sanctuary",
        "D201_1",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0xE, 0x04, "Fire Sanctuary"],
    ),
    "Fire Sanctuary - Second Chest in Water Fruit Room": SSLocData(
        276,
        SSLocFlag.D_FS,
        "Fire Sanctuary",
        "D201_1",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0xD, 0x40, "Fire Sanctuary"],
    ),
    "Fire Sanctuary - Rescue First Trapped Mogma": SSLocData(
        277,
        SSLocFlag.D_FS,
        "Fire Sanctuary",
        "D201_1",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0xD, 0x10, "Fire Sanctuary"],
    ),
    "Fire Sanctuary - Rescue Second Trapped Mogma": SSLocData(
        278,
        SSLocFlag.D_FS,
        "Fire Sanctuary",
        "D201_1",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0x8, 0x20, "Fire Sanctuary"],
    ),
    "Fire Sanctuary - Chest after Bombable Wall": SSLocData(
        279,
        SSLocFlag.D_FS,
        "Fire Sanctuary",
        "D201_1",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0xD, 0x02, "Fire Sanctuary"],
    ),
    "Fire Sanctuary - Plats' Chest": SSLocData(
        280,
        SSLocFlag.D_FS,
        "Fire Sanctuary",
        "D201",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0xC, 0x10, "Fire Sanctuary"],
    ),
    "Fire Sanctuary - Chest in Staircase Room": SSLocData(
        281,
        SSLocFlag.D_FS,
        "Fire Sanctuary",
        "D201",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0x3, 0x02, "Fire Sanctuary"],
    ),
    "Fire Sanctuary - Boss Key Chest": SSLocData(
        282,
        SSLocFlag.D_FS,
        "Fire Sanctuary",
        "D201",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0xB, 0x40, "Fire Sanctuary"],
    ),
    "Fire Sanctuary - Heart Container": SSLocData(
        283,
        SSLocFlag.D_FS,
        "Fire Sanctuary",
        "B201",
        SSLocType.HRTCO,
        [SSLocCheckedFlag.SCENE, 0xE, 0x10, "Fire Sanctuary"],
    ),
    "Fire Sanctuary - Din's Flame": SSLocData(
        284,
        SSLocFlag.D_FS,
        "Fire Sanctuary",
        "B201_1",
        SSLocType.EVENT,
        [SSLocCheckedFlag.SCENE, 0xA, 0x80, "Fire Sanctuary"],
    ),
    # Sky Keep (SK)
    "Sky Keep - First Chest": SSLocData(
        285,
        SSLocFlag.D_SK,
        "Sky Keep",
        "D003_7",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0x3, 0x20, "Sky Keep"],
    ),
    "Sky Keep - Chest after Dreadfuse": SSLocData(
        286,
        SSLocFlag.D_SK,
        "Sky Keep",
        "D003_6",
        SSLocType.T_BOX,
        [SSLocCheckedFlag.SCENE, 0xA, 0x80, "Sky Keep"],
    ),
    "Sky Keep - Rupee in Fire Sanctuary Room in Alcove": SSLocData(
        287,
        SSLocFlag.D_SK | SSLocFlag.RUPEE,
        "Sky Keep",
        "D003_2",
        SSLocType.ITEM,
        [SSLocCheckedFlag.SCENE, 0x5, 0x10, "Sky Keep"],
    ),
    "Sky Keep - Sacred Power of Din": SSLocData(
        288,
        SSLocFlag.D_SK,
        "Sky Keep",
        "D003_8",
        SSLocType.ITEM,
        [SSLocCheckedFlag.SCENE, 0x6, 0x20, "Sky Keep"],  # CHECKTHIS
    ),
    "Sky Keep - Sacred Power of Nayru": SSLocData(
        289,
        SSLocFlag.D_SK,
        "Sky Keep",
        "D003_8",
        SSLocType.ITEM,
        [SSLocCheckedFlag.SCENE, 0x6, 0x40, "Sky Keep"],  # CHECKTHIS
    ),
    "Sky Keep - Sacred Power of Farore": SSLocData(
        290,
        SSLocFlag.D_SK,
        "Sky Keep",
        "D003_8",
        SSLocType.ITEM,
        [SSLocCheckedFlag.SCENE, 0x9, 0x01, "Sky Keep"],  # CHECKTHIS
    ),
    # Silent Realms
    "Skyloft Silent Realm - Trial Reward": SSLocData(
        291,
        SSLocFlag.ALWAYS,
        "Skyloft Silent Realm",
        "S000",
        SSLocType.WPOBJ,
        [SSLocCheckedFlag.STORY, 0xF, 0x01, 0x805A9B30],  # Flag 922
    ),
    "Faron Silent Realm - Trial Reward": SSLocData(
        292,
        SSLocFlag.ALWAYS,
        "Faron Silent Realm",
        "S100",
        SSLocType.WPOBJ,
        [SSLocCheckedFlag.STORY, 0xC, 0x20, 0x805A9B30],  # Flag 919
    ),
    "Lanayru Silent Realm - Trial Reward": SSLocData(
        293,
        SSLocFlag.ALWAYS,
        "Lanayru Silent Realm",
        "S300",
        SSLocType.WPOBJ,
        [SSLocCheckedFlag.STORY, 0xC, 0x80, 0x805A9B30],  # Flag 921
    ),
    "Eldin Silent Realm - Trial Reward": SSLocData(
        294,
        SSLocFlag.ALWAYS,
        "Eldin Silent Realm",
        "S200",
        SSLocType.WPOBJ,
        [SSLocCheckedFlag.STORY, 0xC, 0x40, 0x805A9B30],  # Flag 920
    ),
    # Relics
    "Skyloft Silent Realm - Relic 1": SSLocData(
        295,
        SSLocFlag.TRIAL,
        "Skyloft Silent Realm",
        "S000",
        SSLocType.RELIC,
        [SSLocCheckedFlag.SCENE, 0x0, 0x01, "Skyloft"],  # CHANGE
    ),
    "Skyloft Silent Realm - Relic 2": SSLocData(
        296,
        SSLocFlag.TRIAL,
        "Skyloft Silent Realm",
        "S000",
        SSLocType.RELIC,
        [SSLocCheckedFlag.SCENE, 0x0, 0x01, "Skyloft"],  # CHANGE
    ),
    "Skyloft Silent Realm - Relic 3": SSLocData(
        297,
        SSLocFlag.TRIAL,
        "Skyloft Silent Realm",
        "S000",
        SSLocType.RELIC,
        [SSLocCheckedFlag.SCENE, 0x0, 0x01, "Skyloft"],  # CHANGE
    ),
    "Skyloft Silent Realm - Relic 4": SSLocData(
        298,
        SSLocFlag.TRIAL,
        "Skyloft Silent Realm",
        "S000",
        SSLocType.RELIC,
        [SSLocCheckedFlag.SCENE, 0x0, 0x01, "Skyloft"],  # CHANGE
    ),
    "Skyloft Silent Realm - Relic 5": SSLocData(
        299,
        SSLocFlag.TRIAL,
        "Skyloft Silent Realm",
        "S000",
        SSLocType.RELIC,
        [SSLocCheckedFlag.SCENE, 0x0, 0x01, "Skyloft"],  # CHANGE
    ),
    "Skyloft Silent Realm - Relic 6": SSLocData(
        300,
        SSLocFlag.TRIAL,
        "Skyloft Silent Realm",
        "S000",
        SSLocType.RELIC,
        [SSLocCheckedFlag.SCENE, 0x0, 0x01, "Skyloft"],  # CHANGE
    ),
    "Skyloft Silent Realm - Relic 7": SSLocData(
        301,
        SSLocFlag.TRIAL,
        "Skyloft Silent Realm",
        "S000",
        SSLocType.RELIC,
        [SSLocCheckedFlag.SCENE, 0x0, 0x01, "Skyloft"],  # CHANGE
    ),
    "Skyloft Silent Realm - Relic 8": SSLocData(
        302,
        SSLocFlag.TRIAL,
        "Skyloft Silent Realm",
        "S000",
        SSLocType.RELIC,
        [SSLocCheckedFlag.SCENE, 0x0, 0x01, "Skyloft"],  # CHANGE
    ),
    "Skyloft Silent Realm - Relic 9": SSLocData(
        303,
        SSLocFlag.TRIAL,
        "Skyloft Silent Realm",
        "S000",
        SSLocType.RELIC,
        [SSLocCheckedFlag.SCENE, 0x0, 0x01, "Skyloft"],  # CHANGE
    ),
    "Skyloft Silent Realm - Relic 10": SSLocData(
        304,
        SSLocFlag.TRIAL,
        "Skyloft Silent Realm",
        "S000",
        SSLocType.RELIC,
        [SSLocCheckedFlag.SCENE, 0x0, 0x01, "Skyloft"],  # CHANGE
    ),
    "Faron Silent Realm - Relic 1": SSLocData(
        305,
        SSLocFlag.TRIAL,
        "Faron Silent Realm",
        "S100",
        SSLocType.RELIC,
        [SSLocCheckedFlag.SCENE, 0x0, 0x01, "Skyloft"],  # CHANGE
    ),
    "Faron Silent Realm - Relic 2": SSLocData(
        306,
        SSLocFlag.TRIAL,
        "Faron Silent Realm",
        "S100",
        SSLocType.RELIC,
        [SSLocCheckedFlag.SCENE, 0x0, 0x01, "Skyloft"],  # CHANGE
    ),
    "Faron Silent Realm - Relic 3": SSLocData(
        307,
        SSLocFlag.TRIAL,
        "Faron Silent Realm",
        "S100",
        SSLocType.RELIC,
        [SSLocCheckedFlag.SCENE, 0x0, 0x01, "Skyloft"],  # CHANGE
    ),
    "Faron Silent Realm - Relic 4": SSLocData(
        308,
        SSLocFlag.TRIAL,
        "Faron Silent Realm",
        "S100",
        SSLocType.RELIC,
        [SSLocCheckedFlag.SCENE, 0x0, 0x01, "Skyloft"],  # CHANGE
    ),
    "Faron Silent Realm - Relic 5": SSLocData(
        309,
        SSLocFlag.TRIAL,
        "Faron Silent Realm",
        "S100",
        SSLocType.RELIC,
        [SSLocCheckedFlag.SCENE, 0x0, 0x01, "Skyloft"],  # CHANGE
    ),
    "Faron Silent Realm - Relic 6": SSLocData(
        310,
        SSLocFlag.TRIAL,
        "Faron Silent Realm",
        "S100",
        SSLocType.RELIC,
        [SSLocCheckedFlag.SCENE, 0x0, 0x01, "Skyloft"],  # CHANGE
    ),
    "Faron Silent Realm - Relic 7": SSLocData(
        311,
        SSLocFlag.TRIAL,
        "Faron Silent Realm",
        "S100",
        SSLocType.RELIC,
        [SSLocCheckedFlag.SCENE, 0x0, 0x01, "Skyloft"],  # CHANGE
    ),
    "Faron Silent Realm - Relic 8": SSLocData(
        312,
        SSLocFlag.TRIAL,
        "Faron Silent Realm",
        "S100",
        SSLocType.RELIC,
        [SSLocCheckedFlag.SCENE, 0x0, 0x01, "Skyloft"],  # CHANGE
    ),
    "Faron Silent Realm - Relic 9": SSLocData(
        313,
        SSLocFlag.TRIAL,
        "Faron Silent Realm",
        "S100",
        SSLocType.RELIC,
        [SSLocCheckedFlag.SCENE, 0x0, 0x01, "Skyloft"],  # CHANGE
    ),
    "Faron Silent Realm - Relic 10": SSLocData(
        314,
        SSLocFlag.TRIAL,
        "Faron Silent Realm",
        "S100",
        SSLocType.RELIC,
        [SSLocCheckedFlag.SCENE, 0x0, 0x01, "Skyloft"],  # CHANGE
    ),
    "Lanayru Silent Realm - Relic 1": SSLocData(
        315,
        SSLocFlag.TRIAL,
        "Lanayru Silent Realm",
        "S300",
        SSLocType.RELIC,
        [SSLocCheckedFlag.SCENE, 0x0, 0x01, "Skyloft"],  # CHANGE
    ),
    "Lanayru Silent Realm - Relic 2": SSLocData(
        316,
        SSLocFlag.TRIAL,
        "Lanayru Silent Realm",
        "S300",
        SSLocType.RELIC,
        [SSLocCheckedFlag.SCENE, 0x0, 0x01, "Skyloft"],  # CHANGE
    ),
    "Lanayru Silent Realm - Relic 3": SSLocData(
        317,
        SSLocFlag.TRIAL,
        "Lanayru Silent Realm",
        "S300",
        SSLocType.RELIC,
        [SSLocCheckedFlag.SCENE, 0x0, 0x01, "Skyloft"],  # CHANGE
    ),
    "Lanayru Silent Realm - Relic 4": SSLocData(
        318,
        SSLocFlag.TRIAL,
        "Lanayru Silent Realm",
        "S300",
        SSLocType.RELIC,
        [SSLocCheckedFlag.SCENE, 0x0, 0x01, "Skyloft"],  # CHANGE
    ),
    "Lanayru Silent Realm - Relic 5": SSLocData(
        319,
        SSLocFlag.TRIAL,
        "Lanayru Silent Realm",
        "S300",
        SSLocType.RELIC,
        [SSLocCheckedFlag.SCENE, 0x0, 0x01, "Skyloft"],  # CHANGE
    ),
    "Lanayru Silent Realm - Relic 6": SSLocData(
        320,
        SSLocFlag.TRIAL,
        "Lanayru Silent Realm",
        "S300",
        SSLocType.RELIC,
        [SSLocCheckedFlag.SCENE, 0x0, 0x01, "Skyloft"],  # CHANGE
    ),
    "Lanayru Silent Realm - Relic 7": SSLocData(
        321,
        SSLocFlag.TRIAL,
        "Lanayru Silent Realm",
        "S300",
        SSLocType.RELIC,
        [SSLocCheckedFlag.SCENE, 0x0, 0x01, "Skyloft"],  # CHANGE
    ),
    "Lanayru Silent Realm - Relic 8": SSLocData(
        322,
        SSLocFlag.TRIAL,
        "Lanayru Silent Realm",
        "S300",
        SSLocType.RELIC,
        [SSLocCheckedFlag.SCENE, 0x0, 0x01, "Skyloft"],  # CHANGE
    ),
    "Lanayru Silent Realm - Relic 9": SSLocData(
        323,
        SSLocFlag.TRIAL,
        "Lanayru Silent Realm",
        "S300",
        SSLocType.RELIC,
        [SSLocCheckedFlag.SCENE, 0x0, 0x01, "Skyloft"],  # CHANGE
    ),
    "Lanayru Silent Realm - Relic 10": SSLocData(
        324,
        SSLocFlag.TRIAL,
        "Lanayru Silent Realm",
        "S300",
        SSLocType.RELIC,
        [SSLocCheckedFlag.SCENE, 0x0, 0x01, "Skyloft"],  # CHANGE
    ),
    "Eldin Silent Realm - Relic 1": SSLocData(
        325,
        SSLocFlag.TRIAL,
        "Eldin Silent Realm",
        "S200",
        SSLocType.RELIC,
        [SSLocCheckedFlag.SCENE, 0x0, 0x01, "Skyloft"],  # CHANGE
    ),
    "Eldin Silent Realm - Relic 2": SSLocData(
        326,
        SSLocFlag.TRIAL,
        "Eldin Silent Realm",
        "S200",
        SSLocType.RELIC,
        [SSLocCheckedFlag.SCENE, 0x0, 0x01, "Skyloft"],  # CHANGE
    ),
    "Eldin Silent Realm - Relic 3": SSLocData(
        327,
        SSLocFlag.TRIAL,
        "Eldin Silent Realm",
        "S200",
        SSLocType.RELIC,
        [SSLocCheckedFlag.SCENE, 0x0, 0x01, "Skyloft"],  # CHANGE
    ),
    "Eldin Silent Realm - Relic 4": SSLocData(
        328,
        SSLocFlag.TRIAL,
        "Eldin Silent Realm",
        "S200",
        SSLocType.RELIC,
        [SSLocCheckedFlag.SCENE, 0x0, 0x01, "Skyloft"],  # CHANGE
    ),
    "Eldin Silent Realm - Relic 5": SSLocData(
        329,
        SSLocFlag.TRIAL,
        "Eldin Silent Realm",
        "S200",
        SSLocType.RELIC,
        [SSLocCheckedFlag.SCENE, 0x0, 0x01, "Skyloft"],  # CHANGE
    ),
    "Eldin Silent Realm - Relic 6": SSLocData(
        330,
        SSLocFlag.TRIAL,
        "Eldin Silent Realm",
        "S200",
        SSLocType.RELIC,
        [SSLocCheckedFlag.SCENE, 0x0, 0x01, "Skyloft"],  # CHANGE
    ),
    "Eldin Silent Realm - Relic 7": SSLocData(
        331,
        SSLocFlag.TRIAL,
        "Eldin Silent Realm",
        "S200",
        SSLocType.RELIC,
        [SSLocCheckedFlag.SCENE, 0x0, 0x01, "Skyloft"],  # CHANGE
    ),
    "Eldin Silent Realm - Relic 8": SSLocData(
        332,
        SSLocFlag.TRIAL,
        "Eldin Silent Realm",
        "S200",
        SSLocType.RELIC,
        [SSLocCheckedFlag.SCENE, 0x0, 0x01, "Skyloft"],  # CHANGE
    ),
    "Eldin Silent Realm - Relic 9": SSLocData(
        333,
        SSLocFlag.TRIAL,
        "Eldin Silent Realm",
        "S200",
        SSLocType.RELIC,
        [SSLocCheckedFlag.SCENE, 0x0, 0x01, "Skyloft"],  # CHANGE
    ),
    "Eldin Silent Realm - Relic 10": SSLocData(
        334,
        SSLocFlag.TRIAL,
        "Eldin Silent Realm",
        "S200",
        SSLocType.RELIC,
        [SSLocCheckedFlag.SCENE, 0x0, 0x01, "Skyloft"],  # CHANGE
    ),
    "Hylia's Realm - Defeat Demise": SSLocData(
        None,
        SSLocFlag.ALWAYS,
        "Hylia's Realm",
        "F403",
        SSLocType.EVENT,
        [SSLocCheckedFlag.STORY, 0x0, 0x40, 0x805A9B10],  # Flag 488
        # Set during credits, make sure players go thru the credits at the end
        # Flag 959 is put aside for defeating demise, will be implemented later TODO
    ),
    # HIGHEST_INDEX=334 (Eldin Silent Realm - Relic 10)
    # If you add checks to the list, begin 1 index above the HIGHEST_INDEX
    # and update the value above when you complete
}
