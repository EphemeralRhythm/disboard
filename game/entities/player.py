from game.entities.entity import Entity
from PIL import Image

class Player(Entity):
    def __init__(self, world, db_post):
        super().__init__("player", world)
        self.init_from_db_post(db_post)

        self.player_class = db_post['class']
        self.id = db_post['_id']
        self.gender = db_post['gender']
        self.color = db_post['color']

        self.size = (64, 64)

    def __repr__(self):
        return super().__repr__()

    def draw(self, map_image):
        state = self.stateManager.currentState.name
        flipped = "False"
        frame = "idle"

        if state == "move":
            if self.dir_x == 1:
                flipped = True

            if self.dir_y == 1:
                frame = "up"
            elif self.dir_y == -1:
                frame = "down"
            else:
                frame = "left"

        unit_image = Image.open(f"./assets/images/entities/{self.player_class}/{self.gender}/{self.color}/{frame}.png")

        if flipped:
            unit_image = unit_image.transpose(Image.FLIP_LEFT_RIGHT)

        map_image.paste(unit_image, (self.x - 12, self.y - 16), unit_image)

