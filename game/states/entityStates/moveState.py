from game.states.state import State
from game.entities.entity import Entity
from modules.pathfinding import astar

class MoveState(State):
    def __init__(self, entity: Entity, x, y):
        super().__init__(entity)
        self.entity = entity
        self.name = "move"
        self.path = None
        self.x = x
        self.y = y


    def reached_target(self):
        return self.entity.x == self.x and self.entity.y == self.y

    def OnEnter(self):
        grid = self.entity.world.grid[self.entity.grid_r][self.entity.grid_c]
        path = astar(
            (self.entity.x, self.entity.y),
            (self.x, self.y),
            grid
                     )

        if not path or len(path) == 0:
            self.entity.stateManager.changeState(self.entity.idleState)
            return

        self.path = path[::-1]

    def OnUpdate(self):
        if not self.path:
            self.entity.stateManager.changeState(self.entity.idleState)
            return
        
        self.entity.x = self.path[-1][1]
        self.entity.y = self.path[-1][0]
        self.path.pop()

        print(f"{self.entity.name} is moving.")

    def OnExit(self):
        if self.reached_target():
            print(f"{self.entity.name} reached destination.")
        else:
            print(f"{self.entity.name} failed to reach destination.")
