from game.command import Command
from game.combat.attack import Attack
from game.utils import distance
from copy import deepcopy

from typing import TYPE_CHECKING

from utils.constants import COLOR_BLUE

if TYPE_CHECKING:
    from game.entities.entity import Entity


class Skill:
    def __init__(
        self,
        name,
        cooldown,
        entity: "Entity",
        x: int = 0,
        y: int = 0,
        target=None,
        level: int = 1,
    ):
        self.name = name
        self.cooldown = cooldown
        self.cooldown_timeout = 0
        self.entity = entity

        self.use_range = 15 * 16
        self.range = 16
        self.impact_range = 1

        self.casting_time = 1
        self.casting_timeout = 0

        self.active_time = 1
        self.active_timeout = 0

        self.casting = False
        self.active = False

        self.x = x
        self.y = y
        self.target = target

        self.mana_required = 0
        self.mana_gained = 0

        self.damage_factor = 1
        self.effect_time = 1

        self.crit_rate = 10
        self.crit_multiplier = 1.3

        self.aggro_factor = 1

        self.status_effects = []
        self.crowd_control_state = None

        self.ALLOW_WHILE_STUNNED = False
        self.ALLOW_WHILE_STEALTHED = False
        self.GENERATES_THREAT = True
        self.IS_PASSIVE = False
        self.IS_INTERRUPT = False
        self.IS_DODGEABLE = False
        self.IS_CRITABLE = True
        self.REQUIRES_IN_COMBAT = True
        self.REQUIRES_OUT_OF_COMBAT = True
        self.REMOVES_STEALTH = True
        self.REQUIRES_TARGET = False
        self.REQUIRES_TARGET_OUT_OF_COMBAT = False
        self.REQUIRES_STEALTH = False

        self.prefix = f"## {self.name}\n"
        self.enemy_prefix = (
            self.prefix
            + f"### {self.entity.get_name()} attacked you with the skill **{self.name}**\n"
        )

        self.level = level
        self.init_skill_level()

    def init_skill_level(self):
        pass

    def init_primary_attack(self) -> Attack:
        damage = self.damage_factor * self.entity.get_attack_damage()
        acc = self.entity.get_ACC()

        attack = Attack(damage, acc, source=self.name)
        attack.is_interrupt = self.IS_INTERRUPT
        attack.is_dodgeable = self.IS_DODGEABLE
        attack.is_critable = self.IS_CRITABLE

        attack.crit_rate = self.crit_rate
        attack.crit_multiplier = self.crit_multiplier

        attack.aggro_factor = self.entity.get_aggro_factor() * self.aggro_factor

        attack.enemy_str = self.enemy_prefix

        attack.status_effects = self.status_effects
        attack.crowd_control_state = self.crowd_control_state

        return attack

    def single_target_attack(self):
        if not self.target:
            self.entity.idle()
            return

        attack = self.init_primary_attack()
        notification = self.prefix + self.entity.attack(self.target, attack)
        self.entity.notify(notification, COLOR_BLUE)

    def multi_target_attack(self):
        if not self.entity.cell:
            return

        targets = list(
            filter(
                lambda enemy: distance(self.entity, enemy) <= self.impact_range * 16,
                self.entity.cell.get_targetable_entities(self.entity),
            )
        )

        attack = self.init_primary_attack()
        notification = self.prefix

        for target in targets:
            a: Attack = deepcopy(attack)

            for effect in a.status_effects:
                effect.entity = target

            if a.crowd_control_state:
                a.crowd_control_state.entity = target

            notification += self.entity.attack(target, attack)

        self.entity.notify(notification, COLOR_BLUE)

    def cast(self):
        assert self.casting, "Attempted to update before casting started"

        self.casting_timeout -= 1

        if self.casting_timeout == 0:
            self.activate()
            return True

        return False

    def update(self):
        if self.casting:
            return

        elif self.active:
            self.effect()
            self.active_timeout -= 1

            if self.active_timeout == 0:
                self.active = False
                self.cooldown_timeout = self.cooldown

        elif self.cooldown_timeout > 0:
            self.cooldown_timeout -= 1

    def is_ready(self):
        return not self.active and not self.casting and self.cooldown_timeout == 0

    def use(self):
        assert self.is_ready(), "attempted to use when skill was not ready"
        assert (
            self.entity.MP >= self.mana_required
        ), "Attempted to use skill with insufficient mana"

        self.casting = True
        self.casting_timeout = self.casting_time

        self.entity.lose_MP(self.mana_required)
        print(f"{self.entity} is casting {self.name}.")

    def activate(self):
        self.casting = False
        self.active = True
        self.active_timeout = self.active_time
        self.entity.gain_MP(self.mana_gained)

    def effect(self):
        raise NotImplementedError()

    def __repr__(self):
        name = self.name
        if self.casting:
            name += f" - (Casting, activates in {self.casting_timeout})"
        elif self.active:
            name += f" - (Active, fades in {self.active_timeout})"
        elif self.cooldown_timeout == 0:
            name += " - (Ready)"
        else:
            name += f" - (Available in {self.cooldown_timeout})"

        return name

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, Skill):
            return self.name == __value.name

        return False

    async def initialize(self, player, ctx, client) -> Command | None:
        raise NotImplementedError()
