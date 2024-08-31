import time
from game.world import World
from utils.constants import GAME_TICK


class Backend:
    def __init__(self, world: World) -> None:
        self.world = world
        self.cur_time = 0

    def update_game(self):
        self.world.init_players()
        self.world.init_entities()

        while True:
            if time.time() - self.cur_time >= GAME_TICK:
                self.world.update()
                self.cur_time = time.time()
