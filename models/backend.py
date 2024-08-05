import time
from game.world import World


class Backend:
    def __init__(self, world: World) -> None:
        self.world = world

    def update_game(self):
        self.world.init_players()

        while True:
            self.world.update()
            for player in self.world.get_players():
                print(player)
            time.sleep(10)
