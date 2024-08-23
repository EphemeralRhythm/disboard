from game.entities.entity import Entity
from game.states.state import State
from game.utils import distance
from game.states.mobStates.mobAttackState import MobAttackState
from random import shuffle


class MobIdleState(State):
    def __init__(self, entity):
        super().__init__(entity)
        self.name = "idle"
        self.action_name = "idling"
        self.entity = entity
        self.directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    def OnUpdate(self):
        print(f"{self.entity} is idling.")

        grid = self.entity.cell.terrain
        r, c = self.entity.y // 16, self.entity.x // 16

        cur_height = grid[r][c]
        rows = len(grid)
        cols = len(grid[0])

        shuffle(self.directions)
        for dr, dc in self.directions:
            nr = r + dr
            nc = c + dc

            if nr < 0 or nr >= rows or nc < 0 or nc >= cols:
                continue

            if abs(grid[nr][nc] - cur_height) > 1:
                continue

            self.entity.x = nc * 16
            self.entity.y = nr * 16
            break

        self.entity.update_aggro()
