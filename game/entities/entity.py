import random

from game.states.entityStates.idleState import IdleState
from game.states.state import State
from game.states.stateManager import StateManager
from models.interface.discord_event import DiscordEvent
from utils.constants import COLOR_GREEN, COLOR_RED, COLOR_YELLOW, AUTO_ATTACK_VARIANCE


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
        self.HP = 0
        self.dir_x = 0
        self.dir_y = 0

        self.MAX_HP = 0
        self.MAX_MP = 0
        self.level = 0

        self.HP = 100
        self.DPS = 10

        self.attackRange = 16

        self.directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        self.world = world
        self.cell = self.world.maps[self.grid_r][self.grid_c]

        self.idleState = IdleState(self)
        self.stateManager = StateManager(self, self.idleState)

        self.is_moving = False
        self.is_attacking = False

        self.channel_id = None
        self.skills = []
        self.dead = False

    def __repr__(self):
        return f"{self.name}"

    def init_from_db_post(self, post: dict):
        self.x = post["x"]
        self.y = post["y"]
        self.grid_r = post["grid_r"]
        self.grid_c = post["grid_c"]
        self.HP = post["hp"]

    def init_from_spawn(self, x, y, grid_r, grid_c):
        self.x = x
        self.y = y
        self.grid_r = grid_r
        self.grid_c = grid_c

        self.dir_x, self.dir_y = random.choice(self.directions)
        self.HP = self.MAX_HP

    def update(self):
        if self.dead:
            return

        self.is_moving = False
        self.is_attacking = False

        self.stateManager.update()

        for skill in self.skills:
            skill.update()

    def changeState(self, state: State):
        self.stateManager.changeState(state)

    def get_attack_damage(self):
        return self.DPS

    def is_crit(self):
        # 10% chance of crit rates
        crit_rate = 0.1
        return random.randint(0, 100) >= crit_rate * 100

    def auto_attack(self, entity):
        damage = self.get_attack_damage() * random.randint(
            100 - AUTO_ATTACK_VARIANCE, 100 + AUTO_ATTACK_VARIANCE
        )

        is_crit = self.is_crit()

        if is_crit:
            damage *= 1.5

    def take_damage_from_entity(self, enemy):
        self.HP -= enemy.attackDmage
        print(f"{self} is taking damage from {enemy}. HP is now {self.HP}")

        description = f"You got attacked by {enemy} losing {enemy.attackDamage} HP.\nHP is now {self.HP}."
        self.notify(description, COLOR_RED)

        description = f"Attacked {self} dealing {enemy.attackDamage} DAMAGE.\nEnemy HP is now {self.HP}."
        enemy.notify(description, COLOR_GREEN)

        if self.HP <= 0:
            self.die()

            self.notify("You Died.", COLOR_RED)
            enemy.notify("Target eliminated.", COLOR_RED)
            return True

    def do_damage(self, enemy):
        self.is_attacking = True

    def die(self):
        print(f"{self} dies.")
        self.cell.entities.pop(self)

    def notify(self, description, color=COLOR_YELLOW):
        return

    def update_location(self):
        pass
