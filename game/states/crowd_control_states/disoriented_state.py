from game.states.state import State
from random import shuffle

from utils.constants import COLOR_YELLOW


class DisorientedState(State):
    def __init__(self, entity, timeout):
        super().__init__(entity)

        self.name = "disoriented"
        self.action_name = "disoriented"
        self.is_movement_locked = True
        self.time_remaining = timeout

        self.IS_STATUS_EFFECT = True
        self.directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    def OnUpdate(self):
        self.time_remaining -= 1

        if self.time_remaining == 0:
            self.Exit()

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

        self.time_remaining -= 1

        if self.time_remaining == 0:
            self.Exit()

    def OnExit(self, canceled=False):
        self.entity.notify("You are no longer disoriented.", COLOR_YELLOW)
