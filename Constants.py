# This address is used to check/set the player's health for DeathLink.
CURR_HEALTH_ADDR = 0x8095A76A # HALFWORD

# Link's state- make sure he is not in a loading zone
CURR_STATE_ADDR = 0x80B76585

# The expected index for the following item that should be received. Array of 4 bytes right after the give item array
EXPECTED_INDEX_ADDR = 0x0 # WORD
# WILL BE UPDATED WHEN THE BUILD IS RELEASED

# This address contains the current stage ID.
CURR_STAGE_ADDR = 0x805B388C # STRING[16]

# This is an array of length 0x10 where each element is a byte and contains item IDs for items to give the player.
# 0xFF represents no item. The array is read and cleared every frame.
GIVE_ITEM_ARRAY_ADDR = 0x0 # ARRAY[16]
# WILL BE UPDATED WHEN THE BUILD IS RELEASED

# This is the address that holds the player's file name.
FILE_NAME_ADDR = 0x80955D38 # ARRAY[16]

AP_VISITED_STAGE_NAMES_KEY_FORMAT = "ss_visited_stages_%i"

# Valid addresses for storyflags (ending in zero - final bit is added to this address)
VALID_STORYFLAG_ADDR = [
    0x805A9AD0,
    0x805A9AE0,
    0x805A9AF0,
    0x805A9B00,
    0x805A9B10,
    0x805A9B20,
    0x805A9B30,
]

# Address for the sceneflags for the current stage
CURR_STAGE_SCENEFLAG_ADDR = 0x805A78D0

# Addresses to the sceneflags saved on the current save file
STAGE_TO_SCENEFLAG_ADDR = {
    "Skyloft": 0x80956EC8,
    "Faron Woods": 0x80956ED8,
    "Lake Floria": 0x80956EE8,
    "Flooded Faron Woods": 0x80956EF8,
    "Eldin Volcano": 0x80956F08,
    "Boko Base/Volcano Summit": 0x80956F18,
    "Lanayru Desert": 0x80956F38,
    "Lanayru Sand Sea": 0x80956F48,
    "Lanayru Gorge": 0x80956F58,
    "Sealed Grounds": 0x80956F68,
    "Skyview Temple": 0x80956F78,
    "Ancient Cistern": 0x80956F88,
    "Earth Temple": 0x80956FA8,
    "Fire Sanctuary": 0x80956FB8,
    "Lanayru Mining Facility": 0x80956FD8,
    "Sandship": 0x80956FE8,
    "Sky Keep": 0x80957008,
    "Sky": 0x80957018,
    "Faron Silent Realm": 0x80957028,
    "Eldin Silent Realm": 0x80957038,
    "Lanayru Silent Realm": 0x80957048,
    "Skyloft Silent Realm": 0x80957058,
}

# DME Connection Messages for the client
CONNECTION_REFUSED_GAME_STATUS = (
    "Dolphin failed to connect. Please load a randomized ROM for Skyward Sword. Trying again in 5 seconds..."
)
CONNECTION_REFUSED_SAVE_STATUS = (
    "Dolphin failed to connect. Please load into the save file. Trying again in 5 seconds..."
)
CONNECTION_LOST_STATUS = (
    "Dolphin connection was lost. Please restart your emulator and make sure Skyward Sword is running."
)
CONNECTION_CONNECTED_STATUS = "Dolphin connected successfully."
CONNECTION_INITIAL_STATUS = "Dolphin connection has not been initiated."

OVERWORLD_REGIONS = { # Region: Connected regions
    "Upper Skyloft": ["Central Skyloft", "Sky"],
    "Central Skyloft": ["Upper Skyloft", "Skyloft Village", "Beedle's Shop", "Sky"],
    "Skyloft Village": ["Central Skyloft", "Sky", "Batreaux's House"],
    "Beedle's Shop": ["Central Skyloft"],
    "Batreaux's House": ["Skyloft Village"],
    "Sky": ["Upper Skyloft", "Central Skyloft", "Skyloft Village", "Thunderhead", "Lanayru Mine", "Eldin Volcano", "Sealed Grounds"],
    "Thunderhead": ["Sky"],
    "Sealed Grounds": ["Sky", "Faron Woods", "Hylia's Realm"],
    "Faron Woods": ["Sealed Grounds", "Lake Floria", "Flooded Faron Woods"],
    "Lake Floria": ["Faron Woods"],
    "Flooded Faron Woods": ["Faron Woods"],
    "Eldin Volcano": ["Sky", "Mogma Turf", "Volcano Summit", "Bokoblin Base"],
    "Mogma Turf": ["Eldin Volcano"],
    "Volcano Summit": ["Eldin Volcano"],
    "Bokoblin Base": ["Eldin Volcano"],
    "Lanayru Mine": ["Sky", "Lanayru Desert", "Lanayru Caves"],
    "Lanayru Desert": ["Lanayru Mine", "Lanayru Caves"],
    "Lanayru Caves": ["Lanayru Mine", "Lanayru Desert", "Lanayru Gorge", "Lanayru Sand Sea"],
    "Lanayru Gorge": ["Lanayru Caves"],
    "Lanayru Sand Sea": ["Lanayru Caves"],
    "Hylia's Realm": ["Sealed Grounds"],
}

DUNGEON_HC_CHECKS = {
    "Skyview": "Skyview - Heart Container",
    "Earth Temple": "Earth Temple - Heart Container",
    "Lanayru Mining Facility": "Lanayru Mining Facility - Heart Container",
    "Ancient Cistern": "Ancient Cistern - Heart Container",
    "Sandship": "Sandship - Heart Container",
    "Fire Sanctuary": "Fire Sanctuary - Heart Container",
}

DUNGEON_FINAL_CHECKS = {
    "Skyview": "Skyview - Strike Crest",
    "Earth Temple": "Earth Temple - Strike Crest",
    "Lanayru Mining Facility": "Lanayru Mining Facility - Exit Hall of Ancient Robots",
    "Ancient Cistern": "Ancient Cistern - Farore's Flame",
    "Sandship": "Sandship - Nayru's Flame",
    "Fire Sanctuary": "Fire Sanctuary - Din's Flame",
}

VANILLA_DUNGEON_CONNECTIONS = {
    "Skyview": "dungeon_entrance_in_deep_woods",
    "Earth Temple": "dungeon_entrance_in_eldin_volcano",
    "Lanayru Mining Facility": "dungeon_entrance_in_lanayru_desert",
    "Ancient Cistern": "dungeon_entrance_in_lake_floria",
    "Sandship": "dungeon_entrance_in_lanayru_sand_sea",
    "Fire Sanctuary": "dungeon_entrance_in_volcano_summit",
    "Sky Keep": "dungeon_entrance_on_skyloft",
}

VANILLA_TRIAL_CONNECTIONS = {
    "Skyloft Silent Realm": "trial_gate_on_skyloft",
    "Faron Silent Realm": "trial_gate_in_faron_woods",
    "Eldin Silent Realm": "trial_gate_in_eldin_volcano",
    "Lanayru Silent Realm": "trial_gate_in_lanayru_desert",
}

SWORD_COUNTS = {
    "swordless": 0,
    "practice_sword": 1,
    "goddess_sword": 2,
    "goddess_longsword": 3,
    "goddess_white_sword": 4,
    "master_sword": 5,
    "true_master_sword": 6,
}

POSSIBLE_RANDOM_STARTING_ITEMS = [
    "Progressive Bow",
    "Progressive Beetle",
    "Progressive Slingshot",
    "Progressive Mitts",
    "Progressive Pouch",
    "Bomb Bag",
    "Clawshots",
    "Whip",
    "Gust Bellows",
    "Water Dragon's Scale",
    "Fireshield Earrings",
    "Goddess's Harp",
    "Spiral Charge",
]

BEEDLES_SHOP_VANILLA_ITEMS = {
    "Beedle's Shop - 300 Rupee Item": "Progressive Pouch",
    "Beedle's Shop - 600 Rupee Item": "Progressive Pouch",
    "Beedle's Shop - 1200 Rupee Item": "Progressive Pouch",
    "Beedle's Shop - 800 Rupee Item": "Life Medal",
    "Beedle's Shop - 1600 Rupee Item": "Heart Piece",
    "Beedle's Shop - First 100 Rupee Item": "Extra Wallet",
    "Beedle's Shop - Second 100 Rupee Item": "Extra Wallet",
    "Beedle's Shop - Third 100 Rupee Item": "Extra Wallet",
    "Beedle's Shop - 50 Rupee Item": "Progressive Bug Net",
    "Beedle's Shop - 1000 Rupee Item": "Bug Medal",
}
