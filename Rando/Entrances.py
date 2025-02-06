from typing import TYPE_CHECKING

from Options import OptionError

from ..Locations import LOCATION_TABLE
from ..Options import SSOptions
from ..Constants import *

if TYPE_CHECKING:
    from .. import SSWorld


class EntranceRando:
    """
    Class handles dungeon entrance rando and trial rando.
    """

    def __init__(self, world: "SSWorld"):
        self.world = world
        self.multiworld = world.multiworld

        self.dungeon_connections: dict = {}
        self.trial_connections: dict = {}

        self.dungeons: list[str] = list(VANILLA_DUNGEON_CONNECTIONS.keys())
        self.dungeon_entrances: list[str] = list(VANILLA_DUNGEON_CONNECTIONS.values())
        self.trials: list[str] = list(VANILLA_TRIAL_CONNECTIONS.keys())
        self.trial_gates: list[str] = list(VANILLA_TRIAL_CONNECTIONS.values())

    def randomize_dungeon_entrances(self, req_dungeons: list[str]) -> None:
        """
        Randomize dungeon entrances based on the player's options.
        """

        if self.world.options.randomize_entrances == "none":
            for dun in self.dungeons:
                self.dungeon_connections[dun] = VANILLA_DUNGEON_CONNECTIONS[dun]
        if self.world.options.randomize_entrances == "required_dungeons_separately":
            dungeon_entrances_only_required = [
                VANILLA_DUNGEON_CONNECTIONS[dun]
                for dun in self.dungeons
                if dun in req_dungeons
            ]
            print(req_dungeons)
            print(dungeon_entrances_only_required)
            self.multiworld.random.shuffle(dungeon_entrances_only_required)
            for dun in self.dungeons:
                if dun in req_dungeons:  # TODO CHECK
                    self.dungeon_connections[dun] = (
                        dungeon_entrances_only_required.pop()
                    )
                else:
                    self.dungeon_connections[dun] = VANILLA_DUNGEON_CONNECTIONS[dun]
            print(self.dungeon_connections)
        if self.world.options.randomize_entrances == "all_surface_dungeons":
            dungeon_entrances_no_sky_keep = self.dungeon_entrances.copy()
            dungeon_entrances_no_sky_keep.remove("dungeon_entrance_on_skyloft")
            self.multiworld.random.shuffle(dungeon_entrances_no_sky_keep)
            for dun in self.dungeons:
                if dun != "Sky Keep":
                    self.dungeon_connections[dun] = dungeon_entrances_no_sky_keep.pop()
                else:
                    self.dungeon_connections[dun] = "dungeon_entrance_on_skyloft"
        if (
            self.world.options.randomize_entrances
            == "all_surface_dungeons_and_sky_keep"
        ):
            dungeon_entrances = self.dungeon_entrances.copy()
            self.multiworld.random.shuffle(dungeon_entrances)
            for dun in self.dungeons:
                self.dungeon_connections[dun] = dungeon_entrances.pop()

    def randomize_trial_gates(self) -> None:
        """
        Randomize the trials connected to each trial gate based on the player's options.
        """

        if self.world.options.randomize_trials:
            randomized_trial_gates = self.trial_gates.copy()
            self.multiworld.random.shuffle(randomized_trial_gates)
            for trl in self.trials:
                self.trial_connections[trl] = randomized_trial_gates.pop()
        else:
            for trl in self.trials:
                self.trial_connections[trl] = VANILLA_TRIAL_CONNECTIONS[trl]
