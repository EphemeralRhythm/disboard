from game.states.entityStates.moveState import MoveState
from game.utils import distance

class MobMoveState(MoveState):
    def __init__(self, entity, x, y):
        super().__init__(entity, x, y)
