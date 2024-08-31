from game.states.state import State
from game.utils import distance
from game.entities.entity import Entity
from game.states.entityStates.followState import follow


class MobAttackState(State):
    def __init__(self, entity: Entity, target: Entity):
        super().__init__(entity)
        self.name = "attack"
        self.action_name = "attacking"
        self.entity = entity
        self.target = target

    def OnUpdate(self):
        target = self.target
        entity = self.entity

        if not target or target.is_stealthed() or target.cell != entity.cell:
            self.Exit()
            return

        if distance(target, entity) > entity.attackRange:
            if not follow(entity, target):
                self.Exit()
            return

        entity.is_attacking = True
        print(f"{self.entity} is attacking {self.target}")

        if self.entity.auto_attack(target):
            self.Exit()
            return

        self.entity.update_aggro()
