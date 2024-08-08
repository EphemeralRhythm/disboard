import random
from game.states.state import State
from game.states.entityStates.idleState import IdleState
from game.states.stateManager import StateManager
from models.interface.discord_event import DiscordEvent
from utils.constants import COLOR_RED, COLOR_GREEN


class Entity:
    _last_id = 0
    HOSTILITY_LEVEL_FRIENDLY = 0
    HOSTILITY_LEVEL_NEUTRAL = 1
    HOSTILITY_LEVEL_HOSTILE = 2

    def __init__(self, name, world):

        self.name = name

        Entity._last_id += 1
        self.id = Entity._last_id

        self.hostility_level = Entity.HOSTILITY_LEVEL_NEUTRAL

        self.x = 0
        self.y = 0
        self.grid_r = 0
        self.grid_c = 0
        self.hp = 0
        self.dir_x = 0
        self.dir_y = 0

        self.max_hp = 0
        self.level = 0

        self.directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        self.world = world
        self.cell = self.world.maps[self.grid_r][self.grid_c]

        self.idleState = IdleState(self)
        self.stateManager = StateManager(self, self.idleState)

        self.hp = 100
        self.attackRange = 16
        self.attackDamage = 10

        self.is_moving = False
        self.is_attacking = False

        self.channel_id = None
        self.skills = []

    def __repr__(self):
        return f"{self.name}"

    def init_from_db_post(self, post: dict):
        self.x = post["x"]
        self.y = post["y"]
        self.grid_r = post["grid_r"]
        self.grid_c = post["grid_c"]
        self.hp = post["hp"]

    def init_from_spawn(self, x, y, grid_r, grid_c):
        self.x = x
        self.y = y
        self.grid_r = grid_r
        self.grid_c = grid_c

        self.dir_x, self.dir_y = random.choice(self.directions)
        self.hp = self.max_hp

    def update(self):
        self.is_moving = False
        self.is_attacking = False

        self.stateManager.update()

        for skill in self.skills:
            skill.update()

    def changeState(self, state: State):
        self.stateManager.changeState(state)

    def take_damage_from_entity(self, enemy):
        self.hp -= enemy.attackDamage
        print(f"{self} is taking damage from {enemy}. HP is now {self.hp}")

        if self.name == "player" and self.channel_id:
            title = "You Are Under Attack!"
            description = f"You got attacked by {enemy} losing {enemy.attackDamage} HP.\nHP is now {self.hp}."
            e = DiscordEvent(self.id, self.channel_id, title, description, COLOR_RED)
            self.world.add_event(e)

        if enemy.name == "player" and enemy.channel_id:
            title = "Attacking!"
            description = f"Attacked {self} dealing {enemy.attackDamage} DAMAGE.\nEnemy HP is now {self.hp}."
            e = DiscordEvent(
                enemy.id, enemy.channel_id, title, description, COLOR_GREEN
            )
            self.world.add_event(e)

        if self.hp <= 0:
            self.die()
            return True

    def do_damage(self, enemy):
        self.is_attacking = True

    def die(self):
        print(f"{self} dies.")
