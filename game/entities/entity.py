import random
from game.states.entityStates.idleState import IdleState
from game.states.entityStates.stunnedState import StunnedState
from game.states.state import State
from game.states.stateManager import StateManager
from utils.constants import (
    COLOR_CYAN,
    COLOR_GREEN,
    COLOR_RED,
    COLOR_YELLOW,
    AUTO_ATTACK_VARIANCE,
    ATK_DEF_VARIANCE,
)


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
        self.LEVEL = 0

        self.HP = 100
        self.ATK = 20
        self.AGI = 10
        self.DEF = 10
        self.CRIT = 40

        self.attackRange = 16

        self.directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        self.world = world
        self.cell = self.world.maps[self.grid_r][self.grid_c]

        self.idleState = IdleState(self)
        self.stateManager = StateManager(self, self.idleState)

        self.is_moving = False
        self.is_attacking = False

        self.channel_id = None
        self.dead = False

        self.skills = []
        self.status_effects = []
        self.gear = []

        self.enemies_within_radius = []
        self.aggro_table = {}
        self.aggro_radius = 8
        self.AGGRO_THRESHOLD = 100

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

    def is_movement_locked(self):
        return self.stateManager.currentState.is_movement_locked

    def get_attack_damage(self) -> int:
        """
        base attack damage with all the modifiers
        """
        atk = self.ATK

        for effect in self.status_effects:
            atk += effect.get_ATK_modifier()

        return atk

    def get_input_variance(self, inp: int, variance: int) -> int:
        return int(random.randint(100 - variance, 100 + variance) * inp / 100)

    # damage absorbtion
    def get_DEF(self) -> int:
        _def = self.DEF

        for effect in self.status_effects:
            _def += effect.get_DEF_modifier()

        return _def

    def get_AGI(self) -> int:
        agi = self.AGI

        for effect in self.status_effects:
            agi += effect.get_AGI_modifier()

        return agi

    def get_crit_rate(self) -> int:
        """
        returns a number between 0 and 100
        """
        rate = self.CRIT

        for effect in self.status_effects:
            rate += effect.get_CRIT_modifier()

        return rate

    def roll_crit(self) -> bool:
        # 10% chance of crit rates
        crit_rate = self.get_crit_rate()
        return random.randint(0, 100) >= 100 - crit_rate

    def roll_AGI(self) -> bool:
        """
        returns whether a player succeeds in a dodge
        """

        return random.randint(0, 100) >= 100 - self.get_AGI()

    def roll_DEF(self):
        return self.get_input_variance(self.get_DEF(), ATK_DEF_VARIANCE)

    def auto_attack(self, entity):
        """
        auto attack damage is calculated from modified ATK with a variance percentage
        """

        damage = self.get_input_variance(self.get_attack_damage(), AUTO_ATTACK_VARIANCE)

        is_crit = self.roll_crit()

        if is_crit:
            damage = int(damage * 1.5)

        did_dodge = entity.roll_AGI()

        if did_dodge and not is_crit:
            self.notify(
                f"Attacking {entity}.\n**{entity} dodges** the attack taking no damage.",
                COLOR_YELLOW,
            )
            entity.notify(
                f"You were attacked by {self}.\n**You dodged** the attack taking no damage."
            )

            return

        damage_absorbed = int(entity.roll_DEF())
        damage_dealt = max(damage - damage_absorbed, 0)

        print(f"{entity} is taking damage from {self}. HP is now {entity.HP}")

        self.notify(
            (
                ("**CRITICAL HIT!**\n" if is_crit else "")
                + f"Attacked {entity} **dealing {damage_dealt}** DAMAGE.\nEnemy HP is now **{entity.HP}**."
            ),
            COLOR_GREEN,
        )

        entity.notify(
            ("**CRITICAL HIT**!\n" if is_crit else "")
            + f"You got attacked by {self} **losing {damage_dealt}** HP.\nHP is now **{entity.HP}**.",
            COLOR_RED,
        )

        entity.take_damage(damage_dealt, self)

    def take_damage(self, damage: int, entity=None):
        self.HP -= damage

        if self.HP <= 0:
            self.die()

            if entity:
                entity.notify("Target eliminated", COLOR_CYAN)
            return

        self.OnTakeDamage()

    def OnTakeDamage(self):
        for effect in self.status_effects:
            effect.OnTakeDamage()

        self.stateManager.currentState.OnTakeDamage()

    def die(self):
        # player death is overriden in the player class
        print(f"{self} dies.")
        if self.cell and self.id in self.cell.entities:
            self.cell.entities.pop(self.id)
        self.cell = None

        del self

    def notify(self, description, color=COLOR_YELLOW):
        return

    def update_location(self):
        pass

    def is_silenced(self):
        return any([e.silenced for e in self.status_effects])

    def update_aggro(self):
        pass

    def get_stunned(self, time):
        self.stateManager.changeState(StunnedState(self, time))
