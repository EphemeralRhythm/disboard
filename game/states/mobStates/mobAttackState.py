from game.states.state import State
from game.utils import distance

class MobAttackState(State):
    def __init__(self, entity, target):
        self.name = "attack"
        self.entity = entity
        self.target = target

    def OnUpdate(self):
        target = self.target
        entity = self.entity

        if distance(target, entity) <= entity.attackRange:
            pass
