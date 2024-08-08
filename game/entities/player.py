from game.entities.entity import Entity
from PIL import Image

from game.states.entityStates.moveState import MoveState
from game.states.mobStates.mobAttackState import MobAttackState


class Player(Entity):
    def __init__(self, world, db_post):
        super().__init__("player", world)
        self.init_from_db_post(db_post)

        self.player_class = db_post["class"]
        self.id = db_post["_id"]
        self.gender = db_post["gender"]
        self.color = db_post["color"]

        self.size = (64, 64)
        self.channel_id = db_post.get("channel_id")

    def __repr__(self):
        return self.color + " " + self.player_class

    def draw(self, map_image):
        flipped = "False"
        frame = "idle"

        if self.is_moving:

            if self.dir_y == 1:
                frame = "up"
            elif self.dir_y == -1:
                frame = "down"
            else:
                frame = "left"

        elif self.is_attacking:
            frame = "attack"

        if self.dir_x == 1:
            flipped = True

        unit_image = Image.open(
            f"./assets/images/entities/{self.player_class}/{self.gender}/{self.color}/{frame}.png"
        )

        if flipped:
            unit_image = unit_image.transpose(Image.FLIP_LEFT_RIGHT)

        map_image.paste(unit_image, (self.x - 12, self.y - 16), unit_image)

    def is_ally(self, other_player):
        return False

    def is_movement_locked(self):
        return self.stateManager.currentState.is_movement_locked

    def move(self, x, y):
        self.stateManager.changeState(MoveState(self, x, y))

    def attack(self, target: Entity):
        self.stateManager.changeState(MobAttackState(self, target))
