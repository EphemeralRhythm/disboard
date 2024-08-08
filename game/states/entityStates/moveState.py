from game.states.state import State
from game.entities.entity import Entity
from modules.pathfinding import astar
from game.utils import normalize
from utils.constants import COLOR_GREEN, COLOR_RED
from models.interface.discord_event import DiscordEvent


class MoveState(State):
    def __init__(self, entity: Entity, x, y):
        super().__init__(entity)
        self.entity = entity
        self.name = "move"
        self.path = None
        self.x = x
        self.y = y

    def reached_target(self):
        return (
            self.entity.x // 16 == self.x // 16 and self.entity.y // 16 == self.y // 16
        )

    def OnEnter(self):
        grid = self.entity.cell.terrain
        path = astar((self.entity.x, self.entity.y), (self.x, self.y), grid)

        if not path or len(path) == 0:
            self.Exit()
            return

        print((self.entity.x // 16, self.entity.y // 16), (self.x // 16, self.y // 16))
        self.path = path[::-1]

    def OnUpdate(self):
        if not self.path:
            self.Exit()
            return

        self.entity.dir_x = normalize(self.path[-1][1] * 16 - self.entity.x)
        self.entity.dir_y = normalize(self.entity.y - self.path[-1][0] * 16)

        self.entity.x = self.path[-1][1] * 16
        self.entity.y = self.path[-1][0] * 16

        self.path.pop()
        self.entity.is_moving = True

        print(f"{self.entity} is moving.", self.entity.x // 16, self.entity.y // 16)

    def OnExit(self):
        if self.reached_target():
            print(f"{self.entity} reached destination.")

            if self.entity.name == "player":
                title = "Move command"
                description = "You reached your destination"
                e = DiscordEvent(
                    self.entity.id,
                    self.entity.channel_id,
                    title,
                    description,
                    COLOR_GREEN,
                )
                self.entity.world.add_event(e)
        else:
            print(f"{self.entity} failed to reach destination.")
            if self.entity.name == "player":
                title = "Move command"
                description = "Failed to reach destination."
                e = DiscordEvent(
                    self.entity.id,
                    self.entity.channel_id,
                    title,
                    description,
                    COLOR_RED,
                )
                self.entity.world.add_event(e)
