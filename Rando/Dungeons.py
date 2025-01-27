from typing import TYPE_CHECKING

from Options import OptionError

from ..Locations import LOCATION_TABLE
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
        self.required_dungeons.extend(self.multiword.random.sample(list(DUNGEON_FINAL_CHECKS.keys()), self.num_required_dungeons))
        
        self.required_dungeon_checks.extend([chk for dun, chk in DUNGEON_FINAL_CHECKS.items() if dun in self.required_dungeons])
        self.banned_dungeons.extend([dun for dun in DUNGEON_FINAL_CHECKS.keys() if dun not in self.required_dungeons])

    def dungeon_pre_fill(self) -> None:
        """
        Fills dungeon items based on player's options
        """

        pass # TODO
