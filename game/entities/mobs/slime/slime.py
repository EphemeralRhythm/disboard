from game.entities.mobs.mob import Mob
from PIL import Image


class Slime(Mob):
    def __init__(self, x, y, grid_r, grid_c, world):
        super().__init__("slime", world)

        self.MAX_HP = 200
        self.LEVEL = 30

        self.ATK = 12
        self.size = (32, 32)

        self.init_from_spawn(x, y, grid_r, grid_c)

    def draw(self, map_image, image_draw):
        unit_image = Image.open(
            "./assets/images/entities/player/kannagi/female/purple/idle.png"
        )

        map_image.paste(unit_image, (self.x - 8, self.y - 8), unit_image)

    def __repr__(self):
        return "cleric"
