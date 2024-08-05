from game.entities.mobs.mob import Mob

class Slime(Mob):
    def __init__(self, x, y, grid_r, grid_c, world):
        super().__init__("slime", world)

        self.MAX_HP = 200
        self.LEVEL = 30

        self.init_from_spawn(x, y, grid_r, grid_c)

