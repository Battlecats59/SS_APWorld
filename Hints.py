from enum import Enum, auto
from typing import NamedTuple


class SSHintType(Enum):
    """
    Represents a hint type in Skyward Sword.
    """

    STONE = auto()  # Max 8 hints per stone
    FI = auto()  # Max 64 hints
    SONG = auto()  # Song hints


class SSHint(NamedTuple):
    """
    Represents a hint in Skyward Sword.
    """

    code: int
    region: str
    type: SSHintType


HINT_TABLE: dict[str, SSHint] = {
    "Fi Hint": SSHint(
        0,
        None,
        SSHintType.FI,
    ),
    "Central Skyloft - Gossip Stone on Waterfall Island": SSHint(
        1,
        "Central Skyloft",
        SSHintType.STONE,
    ),
    "Sky - Gossip Stone on Lumpy Pumpkin": SSHint(
        2,
        "Sky",
        SSHintType.STONE,
    ),
    "Sky - Gossip Stone on Volcanic Island": SSHint(
        3,
        "Sky",
        SSHintType.STONE,
    ),
    "Sky - Gossip Stone on Bamboo Island": SSHint(
        4,
        "Sky",
        SSHintType.STONE,
    ),
    "Thunderhead - Gossip Stone near Bug Heaven": SSHint(
        5,
        "Thunderhead",
        SSHintType.STONE,
    ),
    "Sealed Grounds - Gossip Stone behind the Temple": SSHint(
        6,
        "Sealed Grounds",
        SSHintType.STONE,
    ),
    "Faron Woods - Gossip Stone in Deep Woods": SSHint(
        7,
        "Faron Woods",
        SSHintType.STONE,
    ),
    "Lake Floria - Gossip Stone outside Ancient Cistern": SSHint(
        8,
        "Lake Floria",
        SSHintType.STONE,
    ),
    "Eldin Volcano - Gossip Stone next to Earth Temple": SSHint(
        9,
        "Eldin Volcano",
        SSHintType.STONE,
    ),
    "Eldin Volcano - Gossip Stone in Thrill Digger Cave": SSHint(
        10,
        "Eldin Volcano",
        SSHintType.STONE,
    ),
    "Eldin Volcano - Gossip Stone in Lower Platform Cave": SSHint(
        11,
        "Eldin Volcano",
        SSHintType.STONE,
    ),
    "Eldin Volcano - Gossip Stone in Upper Platform Cave": SSHint(
        12,
        "Eldin Volcano",
        SSHintType.STONE,
    ),
    "Volcano Summit - Gossip Stone near Second Thirsty Frog": SSHint(
        13,
        "Volcano Summit",
        SSHintType.STONE,
    ),
    "Volcano Summit - Gossip Stone in Waterfall Area": SSHint(
        14,
        "Volcano Summit",
        SSHintType.STONE,
    ),
    "Temple of Time - Gossip Stone in Temple of Time Area": SSHint(
        15,
        "Lanayru Desert",
        SSHintType.STONE,
    ),
    "Lanayru Sand Sea - Gossip Stone in Shipyard": SSHint(
        16,
        "Lanayru Sand Sea",
        SSHintType.STONE,
    ),
    "Lanayru Caves - Gossip Stone in Center": SSHint(
        17,
        "Lanayru Caves",
        SSHintType.STONE,
    ),
    "Lanayru Caves - Gossip Stone towards Lanayru Gorge": SSHint(
        18,
        "Lanayru Caves",
        SSHintType.STONE,
    ),
    "Song of the Hero - Trial Hint": SSHint(
        19,
        None,
        SSHintType.SONG,
    ),
    "Farore's Courage - Trial Hint": SSHint(
        20,
        None,
        SSHintType.SONG,
    ),
    "Nayru's Wisdom - Trial Hint": SSHint(
        21,
        None,
        SSHintType.SONG,
    ),
    "Din's Power - Trial Hint": SSHint(
        22,
        None,
        SSHintType.SONG,
    ),
}

HINT_DISTRIBUTIONS = {
    "Standard": {
        "Fi": 0,
        "Location": 10,
        "Item": 5,
    }
}

SONG_HINT_TO_TRIAL_GATE = {
    "Song of the Hero - Trial Hint": "trial_gate_on_skyloft",
    "Farore's Courage - Trial Hint": "trial_gate_in_faron_woods",
    "Nayru's Wisdom - Trial Hint": "trial_gate_in_lanayru_desert",
    "Din's Power - Trial Hint": "trial_gate_in_eldin_volcano",
}

JUNK_HINT_TEXT = [
    "They say that crashing in BiT is easy.",
    "They say that bookshelves can talk",
    "They say that people who love the Bug Net also like Trains",
    "They say that there is a Gossip Stone by the Temple of Time",
    "They say there's a 35% chance for Fire Sanctuary Boss Key to be Heetle Locked",
    "They say 64bit left Fire Sanctuary without learning Ballad of the Goddess",
    "They say that Ancient Cistern is haunted by the ghosts of softlocked Links",
    "They say the Potion Lady is still holding onto a Spiral Charge for CJ",
    "They say there is a chest underneath the party wheel in Lanayru",
    "They say that you need the hero's tunic to sleep on the main part of Skyloft",
    "They say that you need to Hot the Spile to defeat Imprisoned 2",
    "They say whenever Spiral Charge is on a trial, a seed roller goes mysteriously missing",
    "They say that Eldin Trial is vanilla whenever it is required",
    "They say that gymnast86 won the first randomizer tournament and retired immediately after",
    "They say that Mogmas don't understand Minesweeper",
    "They say that you can win a race by abandoning Lanayru to check Cawlin's Letter",
    "They say that tornados spawn frequently in the Sky",
    "They say Scrapper gets easily tilted",
    "They say there is a chest on the cliffs by the Goddess Statue",
    "They say that entering Ancient Cistern with no B items has a 1% chance of success",
    "They say that Glittering Spores are the best bird drugs",
    "They say that the Ancient Automaton fears danger darts",
    "They say the single tumbling plant is required every seed",
    "They say that your battery is low",
    "They say that you just have to get the right checks to win",
    "They say that rushing Peatrice is the play",
    "They say there is a 0.0000001164% chance your RNG won't change",
    "If only we could go Back in Time and name the glitch properly...",
    'They say that there is something called a "hash" that makes it easier for people to verify that they are playing the right seed',
    "They say that the bad seed rollers are still in the car, seeking for a safe refugee",
    "Have you heard the tragedy of Darth Kolok the Pause? I thought not, it's not a story the admins would tell you",
    "Lanayru Sand Sea is the most hated region in the game, because Sand is coarse, rough and gets everywhere",
    "They say that rice has magical properties when visiting Yerbal",
    "They say that Jannon is still jammin to this day",
    "They say that there is only one place where the Slingshot beats the Bow",
    "They say that Koloktos waiting caused a civil war among players",
    "They say that there is a settings combination which needs 0 checks to be completed",
    "They say that avoiding Fledge's item from a fresh file is impossible",
    "... astronomically ...",
    "They say that you can open the chest behind bars in LMF after raising said bars",
    "They say that you look like you have a Questions",
    "They say that HD randomizer development is delayed by a day every time someone asks about it in the Discord",
    "The disc could not be read. Refer to the Wii Operations Manual for details.",
    "They say that a massive storm brews over the Lanayru Sand Sea due to Tentalus' immense size",
]
