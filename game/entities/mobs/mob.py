from game.entities.entity import Entity
from game.states.mobStates.mobIdleState import MobIdleState
from game.states.stateManager import StateManager

class Mob(Entity):
    def __init__(self, name, world):
        self.idleState = MobIdleState(self)
        super().__init__(name, world)

        self.isHostile = False 
        self.aggroRadius = 18
        self.attackRange = 16

        self.idleState = MobIdleState(self)
        self.stateManager = StateManager(self, self.idleState)
