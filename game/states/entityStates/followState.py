from game.states.state import State
from game.entities.entity import Entity
from modules.pathfinding import astar
from game.utils import normalize


def follow(entity: Entity, target: Entity):
    if entity.cell != target.cell:
        return False

    grid = entity.cell.terrain
    path = astar((entity.x, entity.y), (target.x, target.y), grid)

    if not path or len(path) == 0:
        entity.update_location()
        return entity.x // 16 == target.x // 16 and entity.y // 16 == target.y // 16

    entity.dir_x = normalize(path[-1][1] * 16 - entity.x)
    entity.dir_y = normalize(entity.y - path[-1][0] * 16)

    entity.x = path[0][1] * 16
    entity.y = path[0][0] * 16

    entity.is_moving = True
    print(f"{entity} is following {target}.")

    return True


class FollowState(State):
    def __init__(self, entity: Entity, target: Entity):
        super().__init__(entity)
        self.entity = entity
        self.target = target
        self.name = "follow"
        self.action_name = "following"
        self.path = None

    def reached_target(self):
        return (
            self.entity.x // 16 == self.target.x // 16
            and self.entity.y // 16 == self.target.y // 16
        )

    def OnUpdate(self):
        if not follow(self.entity, self.target):
            self.Exit()

    def OnExit(self, canceled=False):
        if self.reached_target():
            print(f"{self.entity} reached destination.")
        else:
            print(f"{self.entity} failed to reach destination.")
