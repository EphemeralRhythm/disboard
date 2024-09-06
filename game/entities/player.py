from game.entities.entity import Entity
from PIL import Image, ImageEnhance

from game.states.entityStates.attackState import AttackState
from game.states.entityStates.moveState import MoveState
from game.states.entityStates.castState import CastState

from modules.player_loader import update_skills


from utils.constants import COLOR_YELLOW

import utils.database as db
from models.interface.discord_event import DiscordEvent


class Player(Entity):
    def __init__(self, world, db_post):
        super().__init__("player", world)
        self.init_from_db_post(db_post)

        self.username = db_post["username"]
        self.player_class = db_post["class"]
        self.id = db_post["_id"]
        self.gender = db_post["gender"]
        self.color = db_post["color"]
        self.LEVEL = db_post["level"]

        self.size = (32, 32)
        self.channel_id = db_post.get("channel_id")

        self.attackRange = 16

        self.HP = 11360
        self.ATK = 570
        self.DEF = 200
        self.CRIT = 60

        self.MAX_HP = self.HP

        update_skills(self)

    def __repr__(self):
        return (self.color + " " + self.player_class).title()

    def get_name(self):
        return f"<@{self.id}>"

    def draw(self, map_image, image_draw):
        flipped = False
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
            f"./assets/images/entities/player/{self.player_class}/{self.gender}/{self.color}/{frame}.png"
        )

        if flipped:
            unit_image = unit_image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)

        if self.is_stealthed():
            alpha = unit_image.split()[3]
            alpha = ImageEnhance.Brightness(alpha).enhance(0.5)
            unit_image.putalpha(alpha)

        map_image.paste(unit_image, (self.x - 8, self.y - 8), unit_image)

    def draw_gui(self, map_image, image_draw):
        super().draw_gui(map_image, image_draw)

    def is_ally(self, other_player):
        return False

    def change_to_move_state(self, x, y):
        self.stateManager.changeState(MoveState(self, x, y), True)

    def change_to_attack_state(self, target: Entity):
        self.stateManager.changeState(AttackState(self, target), True)

    def cast(self, skill):
        self.stateManager.changeState(
            CastState(self, skill, self.stateManager.currentState)
        )

    def notify(self, description, color=COLOR_YELLOW):
        if self.name != "player" or not self.channel_id:
            return

        e = DiscordEvent(
            self.id,
            self.channel_id,
            description,
            color,
        )

        self.world.add_event(e)

    def die(self):
        self.dead = True
        if self.cell:
            self.cell.remove_player(self)
            self.cell = self.world.dead_pool

        self.notify("**You died.**\nYour deeds of heroism will be remembered.")

    def update_location(self):
        db.players_collection.update_one(
            {"_id": self.id},
            {
                "$set": {
                    "x": self.x,
                    "y": self.y,
                    "grid_r": self.grid_r,
                    "grid_c": self.grid_c,
                }
            },
        )

    def get_stunned(self, time):
        super().get_stunned(time / 2)

    def get_disoriented(self, time):
        super().get_disoriented(time / 2)
