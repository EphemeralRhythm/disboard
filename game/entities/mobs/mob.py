from game.entities.entity import Entity
from game.states.mobStates.mobIdleState import MobIdleState
from game.states.stateManager import StateManager
from game.utils import distance
from collections import defaultdict


class Mob(Entity):
    def __init__(self, name, world):
        super().__init__(name, world)

        self.aggro_radius = 18

        self.idleState = MobIdleState(self)
        self.stateManager = StateManager(self, self.idleState)

        self.aggro_table = defaultdict(int)
        self.AGGRO_THRESHOLD = 100

    def update_aggro(self):
        players = self.cell.players

        for player in players:
            dist = distance(self, player)
            level_diff = self.LEVEL - player.LEVEL

            if dist < self.aggro_radius:
                self.aggro_table[player.id] += level_diff * 5 + (100 / dist)
