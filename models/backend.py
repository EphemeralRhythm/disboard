import time
from game.world import World
from utils.constants import GAME_TICK


class Backend:
    def __init__(self, world: World) -> None:
        self.world = world

    def update_game(self):
        self.world.init_players()

        while True:
            self.world.update()
            time.sleep(GAME_TICK)
