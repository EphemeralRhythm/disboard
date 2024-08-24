from game.entities.entity import Entity
from PIL import Image, ImageEnhance

from game.skills.generic.shield_bash import ShieldBash
from game.states.entityStates.attackState import AttackState
from game.states.entityStates.moveState import MoveState
from game.states.entityStates.castState import CastState

from game.skills.generic.fireball import Fireball
from game.skills.classes.assassin.ghost_step import GhostStep
from game.skills.classes.assassin.shadow_cloak import ShadowCloak
from game.skills.classes.assassin.phantom_blink import PhantomBlink

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

        self.size = (32, 32)
        self.channel_id = db_post.get("channel_id")

        fireball = Fireball(self)
        shield_bash = ShieldBash(self)
        ghost_step = GhostStep(self)
        shadow_cloak = ShadowCloak(self)
        phantom_blink = PhantomBlink(self)

        self.skills = [fireball, shield_bash, ghost_step, shadow_cloak, phantom_blink]

        self.attackRange = 500
        self.ATK = 20

    def __repr__(self):
        return (self.color + " " + self.player_class).title()

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

    def is_ally(self, other_player):
        return False

    def move(self, x, y):
        self.stateManager.changeState(MoveState(self, x, y), True)

    def attack(self, target: Entity):
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

        self.notify("You died")

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
