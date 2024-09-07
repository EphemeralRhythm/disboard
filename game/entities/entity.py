import random
from typing import List, TYPE_CHECKING

from game.states.entityStates.idleState import IdleState
from game.states.crowd_control_states.stunned_state import StunnedState
from game.states.crowd_control_states.disoriented_state import DisorientedState
from game.states.state import State
from game.states.stateManager import StateManager

from game.utils import randomize, random_roll
from game.combat.attack import Attack

from utils.constants import (
    COLOR_CYAN,
    COLOR_GREEN,
    COLOR_RED,
    COLOR_YELLOW,
    AUTO_ATTACK_VARIANCE,
    ATK_DEF_VARIANCE,
)

from utils.game import icons_emoji

if TYPE_CHECKING:
    from game.skills.skill import Skill
    from game.status_effects.status_effect import StatusEffect


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
        self.dir_x = 0
        self.dir_y = 0

        self.HP = 0
        self.MP = 0

        self.MAX_HP = 100
        self.MAX_MP = 100
        self.LEVEL = 0

        self.HP = 100
        self.ATK = 20
        self.DODGE = 10
        self.ACC = 10
        self.DEF = 10
        self.CRIT = 30
        self.attackRange = 16
        self.CRIT_MULTIPLIER = 1.5

        self.combat_cooldown = 20
        self.combat_timeout = 0

        self.directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        self.world = world
        self.cell = self.world.maps[self.grid_r][self.grid_c]

        self.idleState = IdleState(self)
        self.stateManager = StateManager(self, self.idleState)

        self.is_moving = False
        self.is_attacking = False

        self.channel_id = None
        self.dead = False

        self.skills: List["Skill"] = []
        self.status_effects: List["StatusEffect"] = []
        self.gear = []

        self.aggro_factor = 1
        self.enemies_within_radius = []
        self.aggro_table = {}
        self.aggro_radius = 8
        self.AGGRO_THRESHOLD = 100

    def __repr__(self):
        return f"{self.name}"

    def get_name(self):
        return f"{self.name}"

    def init_from_db_post(self, post: dict):
        self.x = post["x"]
        self.y = post["y"]
        self.grid_r = post["grid_r"]
        self.grid_c = post["grid_c"]
        self.HP = post["hp"]

        self.dir_x = 0
        self.dir_y = -1

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

        if t := self.combat_timeout != 0:
            self.combat_timeout -= 1

            if t == 1:
                self.on_leave_combat()

        self.stateManager.update()

        for skill in self.skills:
            skill.update()

        effects = []
        for e in self.status_effects:
            if e.update():
                effects.append(e)
        self.status_effects = effects

    def idle(self):
        self.stateManager.changeState(self.idleState)

    def interrupt(self, entity=None):
        if self.stateManager.currentState.name == "casting":
            self.idle()
            self.notify(
                "Your casting was interrupted" + f" by {entity.get_name()}."
                if entity
                else "."
            )
            return True

        return False

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

    def get_DEF(self) -> int:
        _def = self.DEF

        for effect in self.status_effects:
            _def += effect.get_DEF_modifier()

        return _def

    def get_DODGE(self) -> int:
        agi = self.DODGE

        for effect in self.status_effects:
            agi += effect.get_DODGE_modifier()

        return agi

    def get_ACC(self) -> int:
        """
        returns attack accuracy with all the modifiers
        """
        acc = self.ACC

        for effect in self.status_effects:
            acc += effect.get_ACC_modifier()

        return acc

    def get_crit_rate(self) -> int:
        """
        returns crit rate (percentage) with all modifiers added
        """
        rate = self.CRIT

        for effect in self.status_effects:
            rate += effect.get_CRIT_modifier()

        return rate

    def on_critical(self, source: str):
        pass

    def enter_combat(self):
        if self.combat_timeout == 0:
            self.on_enter_combat()

        self.combat_timeout = self.combat_cooldown

    def on_enter_combat(self):
        pass

    def on_leave_combat(self):
        pass

    def get_aggro_factor(self):
        aggro = self.aggro_factor

        for effect in self.status_effects:
            aggro *= effect.get_aggro_modifier()

        return aggro

    def roll_crit(self) -> bool:
        crit_rate = self.get_crit_rate()
        return random.randint(0, 100) <= crit_rate

    def roll_DODGE(self, enemy_acc) -> bool:
        """
        returns whether a player succeeds in a dodge
        """

        return random_roll((self.get_DODGE() / enemy_acc) * 40)

    def roll_DEF(self):
        return randomize(self.get_DEF(), ATK_DEF_VARIANCE)

    def auto_attack(self, enemy: "Entity"):
        self.remove_stealth()

        self_str = f"### {icons_emoji['attack']} Attacking {enemy.get_name()}\n"
        enemy_str = (
            f"### {icons_emoji['attack']} You were attacked by {self.get_name()}\n"
        )

        attack = Attack(self.get_attack_damage(), self.get_ACC(), source="auto attack")
        attack.enemy_str = enemy_str
        attack.attacker = self

        attack.crit_rate = self.get_crit_rate()

        self_str += self.attack(enemy, attack)
        self.notify(self_str, COLOR_GREEN)

        print(f"{enemy} is taking damage from {self}. HP is now {enemy.HP}")

    def calculate_damage_dealt(self, damage: int):
        damage_absorbed = int(self.roll_DEF())
        damage_dealt = max(damage - damage_absorbed, 0)

        return damage_dealt

    def gain_aggro(self, aggro: int, entity: "Entity"):
        pass

    def attack(self, enemy: "Entity", attack: Attack) -> str:

        self_str = f"### ■ {enemy.get_name().title()}\n"
        enemy_str = attack.enemy_str

        is_crit = random_roll(attack.crit_rate) and attack.is_critable

        did_dodge = attack.is_dodgeable and (not is_crit) and enemy.roll_DODGE(self.ACC)

        if did_dodge:
            self_str += "- **Dodged the attack**"
            enemy_str += "**You dodged** the attack taking no damage."
            enemy.notify(enemy_str, COLOR_YELLOW)

            return self_str

        damage = randomize(attack.damage, attack.variance)
        damage = enemy.calculate_damage_dealt(damage)

        if is_crit:
            self_str += "- **Critical Hit!**\n"
            enemy_str += "- **Critical Hit!**\n"

            damage *= attack.crit_multiplier

        if damage != 0:
            enemy.HP -= damage
            self_str += f"- **Damage Dealt:** {damage}\n"
            enemy_str += f"- **Damage Received:** {damage}\n"

            enemy.on_take_damage()
            self.enter_combat()

        hp_str = f"- **HP Remaining:** {enemy.HP}/{enemy.MAX_HP}, ({int(enemy.HP / enemy.MAX_HP * 100)} %)\n"

        self_str += hp_str
        enemy_str += hp_str

        status_effects = attack.status_effects
        crowd_control = attack.crowd_control_state

        if attack.is_interrupt:
            if enemy.interrupt(attack.attacker):
                self_str += "- **Interrupted casting**\n"

        enemy.gain_aggro(int(damage * attack.aggro_factor), self)

        if status_effects:
            status_effects_str = "- **Status Effects:** "

            for effect in status_effects:
                status_effects_str += effect.__repr__() + " "
                enemy.add_status_effect(effect)

            self_str += status_effects_str + "\n"
            enemy_str += status_effects_str + "\n"

        if crowd_control:
            crowd_control_str = f"- **Crowd Control Effects:** {crowd_control}\n"

            self_str += crowd_control_str
            enemy_str += crowd_control_str

            enemy.stateManager.changeState(crowd_control)

        enemy.notify(enemy_str, COLOR_RED)

        if enemy.HP <= 0:
            enemy.die()
            self_str += "- **Target Eliminated**\n"

        return self_str

    def heal(self, heal_amount):
        self.HP = min(self.MAX_HP, self.HP + heal_amount)

    def on_take_damage(self):
        self.enter_combat()

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

    def lose_MP(self, amount):
        assert self.MP >= amount, "tried to subtract more mana than the entity has"
        self.MP -= amount

    def gain_MP(self, amount):
        self.MP = min(self.MAX_MP, self.MP + amount)

    def notify(self, description, color=COLOR_YELLOW):
        return

    def update_location(self):
        pass

    def add_status_effect(self, e):
        for effect in self.status_effects:
            if e.name == effect.name:
                effect.renew(e.remaining_time)
                break
        else:
            self.status_effects.append(e)

    def is_silenced(self):
        return any([e.silenced for e in self.status_effects])

    def is_stealthed(self):
        return any([e.name == "stealth" for e in self.status_effects])

    def is_in_combat(self):
        return self.combat_timeout != 0

    def remove_stealth(self):
        self.status_effects = list(
            filter(lambda x: x.name != "stealth", self.status_effects)
        )

    def update_aggro(self):
        pass

    def get_stunned(self, time):
        self.stateManager.changeState(StunnedState(self, time))

    def get_disoriented(self, time):
        self.stateManager.changeState(DisorientedState(self, time))

    def draw(self, map_image, image_draw):
        raise NotImplementedError()

    def draw_gui(self, map_image, image_draw):
        self.draw_hp_bar(map_image, image_draw)

    def draw_hp_bar(self, map_image, image_draw):
        node_x = self.x - self.x % 16
        node_y = self.y - self.y % 16 - 6

        # draw outline
        image_draw.rectangle((node_x, node_y, node_x + 16, node_y + 2), fill="black")

        # draw red
        image_draw.rectangle(
            (node_x + 1, node_y + 1, node_x + 15, node_y + 1), fill=(255, 0, 0)
        )

        hp = int(self.HP / self.MAX_HP * 14)
        # draw green
        image_draw.rectangle(
            (node_x + 1, node_y + 1, node_x + hp + 1, node_y + 1), fill=(0, 255, 0)
        )
