from game.entities.entity import Entity
from game.states.state import State
from game.utils import distance
from game.entities.mobs.mob import Mob
from game.states.mobStates.mobAttackState import MobAttackState


class MobIdleState(State):
    def __init__(self, entity: Mob):
        super().__init__(entity)
        self.name = "idle"
        self.action_name = "idling"
        self.entity = entity

    def OnUpdate(self):
        table = self.entity.aggro_table

        if len(table) == 0 or (mx := max(table.values())) < self.entity.AGGRO_THRESHOLD:
            return

        players = [(_id, table[_id]) for _id in table.values()]

        players.sort(key=lambda a: a[1])

        cell = self.entity.cell
        _id = players[-1][0]
        player = None
        while players:
            player = self.entity.world.get_player(_id)

            if not player or player.cell != cell:
                players.pop()
            else:
                break

        if not player:
            return

        self.entity.stateManager.changeState(MobAttackState(self.entity, player))
