from typing import TYPE_CHECKING

from BaseClasses import ItemClassification as IC

from ..Hints import SSHint, SSHintType, HINT_TABLE, SONG_HINT_TO_TRIAL_GATE, JUNK_HINT_TEXT
from ..Items import ITEM_TABLE
from ..Locations import LOCATION_TABLE

if TYPE_CHECKING:
    from .. import SSWorld


def handle_hints(world: "SSWorld") -> dict[str, list]:
    """
    Handles hints for Skyward Sword during the APSSR file output.

    :param world: The SS game world.
    :return: Dict containing hints for Fi, each Gossip Stone, and songs.
    """
    hints: dict[str, list] = {}

    for hint, data in HINT_TABLE.items():
        if data.type == SSHintType.FI:
            hints["Fi"] = []
        elif data.type == SSHintType.STONE:
            hints[hint] = _get_junk_hint_texts(world, 2)
        elif data.type == SSHintType.SONG:
            hints[hint] = _handle_song_hints(world, hint)

    return hints


def handle_impa_sot_hint(world: "SSWorld") -> tuple[str, str] | None:
    """
    Handles Impa's Stone of Trials hint.
    """
    sot_locations = [
        loc
        for loc in world.multiworld.get_locations()
        if loc.item.player == world.player and loc.item.name == "Stone of Trials"
    ]
    if len(sot_locations) == 1:
        sot_location = sot_locations.pop()
        return (sot_location.parent_region.name, world.multiworld.get_player_name(sot_location.player))
    else:
        return None


def _handle_song_hints(world: "SSWorld", hint) -> list[str]:
    direct_text = "This trial holds {plr}'s {itm}"
    required_text = "Your spirit will grow by completing this trial"
    useful_text = "Someone might need its reward..."
    useless_text = "Its reward is probably not too important..."

    trial_gate = SONG_HINT_TO_TRIAL_GATE[hint]
    trial_connection = [trl for trl, gate in world.entrances.trial_connections.items() if gate == trial_gate].pop()
    trial_item = world.get_location(f"{trial_connection} - Trial Reward").item
    if world.options.song_hints == "none":
        return [""]
    if world.options.song_hints == "basic":
        return [useful_text] if trial_item.classification == IC.progression or trial_item.classification == IC.useful else [useless_text]
    if world.options.song_hints == "advanced":
        if trial_item.classification == IC.progression:
            return [required_text]
        elif trial_item.classification == IC.useful:
            return [useful_text]
        else:
            return [useless_text]
    if world.options.song_hints == "direct":
        player_name = world.multiworld.get_player_name(trial_item.player)
        item_name = trial_item.name
        return [direct_text.format(plr=player_name, itm=item_name)]


def _get_junk_hint_texts(world: "SSWorld", q: int) -> list[str]:
    """
    Get q number of junk hint texts.

    :param world: The SS game world.
    :param q: Quantity of junk hints to return.
    :return: List of q junk hints.
    """
    return world.multiworld.per_slot_randoms[world.player].sample(JUNK_HINT_TEXT, k=q)
