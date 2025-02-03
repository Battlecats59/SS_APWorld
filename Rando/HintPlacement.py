from typing import TYPE_CHECKING

from ..Hints import SSHint, SSHintType, HINT_TABLE, JUNK_HINT_TEXT
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
            hints[hint] = [""]

    return hints


def _get_junk_hint_texts(world: "SSWorld", q: int) -> list[str]:
    """
    Get q number of junk hint texts.

    :param world: The SS game world.
    :param q: Quantity of junk hints to return.
    :return: List of q junk hints.
    """
    return world.multiworld.per_slot_randoms[world.player].sample(JUNK_HINT_TEXT, k=q)
