from game.states.state import State
from game.entities.entity import Entity
from modules.pathfinding import astar


def follow(entity: Entity, target: Entity):
    if entity.cell != target.cell:
        return False

    grid = entity.cell.terrain
    path = astar((entity.x, entity.y), (target.x, target.y), grid)

    if not path or len(path) == 0:
        return False

    entity.x = path[0][1] * 16
    entity.y = path[0][0] * 16

    print(f"{entity.name} is following {target.name}.")

    return True


class FollowState(State):
    def __init__(self, entity: Entity, target: Entity):
        super().__init__(entity)
        self.entity = entity
        self.target = target
        self.name = "follow"
        self.path = None

    def reached_target(self):
        return (
            self.entity.x // 16 == self.target.x // 16
            and self.entity.y // 16 == self.target.y // 16
        )

    def OnUpdate(self):
        if not follow(self.entity, self.target):
            self.Exit()

    def OnExit(self):
        if self.reached_target():
            print(f"{self.entity.name} reached destination.")
        else:
            print(f"{self.entity.name} failed to reach destination.")
