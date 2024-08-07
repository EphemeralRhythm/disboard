from game.states.state import State
from game.utils import distance
from game.entities.entity import Entity
from game.states.entityStates.followState import follow


class MobAttackState(State):
    def __init__(self, entity: Entity, target: Entity):
        self.name = "attack"
        self.entity = entity
        self.target = target

    def OnUpdate(self):
        target = self.target
        entity = self.entity

        if target.cell != entity.cell:
            self.Exit()
            return

        if distance(target, entity) > entity.attackRange:
            if not follow(entity, target):
                self.Exit()
            return

        entity.do_damage(target)

        if target.take_damage_from_entity(entity):
            self.Exit()
