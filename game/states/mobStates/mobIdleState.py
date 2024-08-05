from game.entities.entity import Entity
from game.states.state import State
from game.utils import distance
from game.states.mobStates.mobAttackState import MobAttackState

class MobIdleState(State):
    def __init__(self, entity: Entity):
        super().__init__(entity)
        self.name = "idle"

    def OnUpdate(self):
        entity = self.entity
        
        players = entity.world.grid[entity.grid_r][entity.grid_c].players
        aggroPlayers = []

        for player in players:
            dist = distance(entity, player)
            level_diff = max(entity.LEVEL, player.level)
            level_diff = level_diff / 30 + 1

            aggro = (1/ dist) * 18
            if aggro >= 1:
                aggroPlayers.append((aggro, player))

        aggroPlayers.sort(key = lambda x: x[0])

        if aggroPlayers[-1][0] >= 1:
            entity.changeState(MobAttackState(entity, aggroPlayers[-1][1]))
