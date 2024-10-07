from game.combat.support import Support
from game.command import Command
from game.combat.attack import Attack
from game.utils import distance
from copy import deepcopy
import discord

from typing import TYPE_CHECKING, List

from utils.constants import COLOR_BLUE, COLOR_CYAN

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

        self.heal_factor = 1

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
        self.REQUIRES_IN_COMBAT = False
        self.REQUIRES_OUT_OF_COMBAT = False
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

        self.support_heal = 0
        self.support_mana = 0

    def init_skill_level(self):
        pass

    def init_primary_attack(self) -> Attack:
        damage = self.damage_factor * self.entity.get_attack_damage()
        acc = self.entity.get_ACC()

        attack = Attack(damage, acc, source=self)
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

    def init_support(self) -> Support:
        heal = self.support_heal
        mana = self.support_mana

        sprt = Support(heal, mana, self)
        sprt.status_effects = self.status_effects

        return sprt

    def notify_mana(self) -> str:
        notification = "\n## Mana"
        notification += f"\nMana gained: {self.mana_gained}"
        notification += f"\nYour Mana: {self.entity.MP}"
        return notification

    def single_target_attack(self):
        if not self.target:
            self.entity.idle()
            return

        attack = self.init_primary_attack()
        notification = self.prefix + self.entity.attack(self.target, attack)

        if self.mana_gained != 0:
            notification += self.notify_mana()

        self.entity.notify(notification, COLOR_BLUE)

    def single_target_support(self):
        if not self.target:
            self.entity.idle()
            return

        sprt = self.init_support()

        self.entity.support(self.target, sprt)

    def multi_target_attack(self):
        if not self.entity.cell:
            self.entity.idle()
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

        if self.mana_gained != 0:
            notification += self.notify_mana()
        self.entity.notify(notification, COLOR_BLUE)

        return targets

    def multi_target_support(self):
        if not self.entity.cell:
            self.entity.idle()
            return

        targets = list(
            filter(
                lambda e: distance(self.entity, e) <= self.impact_range * 16,
                self.entity.cell.get_allied_entities(self.entity),
            )
        )

        sprt = self.init_support()

        for target in targets:
            a: Support = deepcopy(sprt)

            for effect in a.status_effects:
                effect.entity = target

            self.entity.support(target, a)

        return targets

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

    async def initialize(self, player, ctx, client, arg=None) -> Command | None:
        raise NotImplementedError()

    def get_info_embed(self):
        embed = discord.Embed(color=COLOR_CYAN, title=self.name)
        description = self.__doc__ or ""
        description += "\n"

        description += f"- Cooldown: {self.cooldown}\n"
        if self.mana_required:
            description += f"- Requires mana: {self.mana_required} MP\n"
        if self.mana_gained:
            description += f"- Generates mana: {self.mana_required} MP\n"

        if self.status_effects:
            description += "\n"
        for effect in self.status_effects:
            description += f"- Inflicts: {effect}\n"

        if self.crowd_control_state:
            description += f"- Inflicts: {self.crowd_control_state}\n"

        description += "\n"

        for attr in dir(self):
            if not attr.isupper() or not getattr(self, attr):
                continue

            description += f"- {attr}\n"

        embed.description = description
        return embed

    def get_enemies(self, client, player, x, y) -> List["Entity"]:
        return client.world.get_targetable_entities(player, x, y)

    def get_allies(self, client, player, x, y) -> List["Entity"]:
        return client.world.get_targetable_entities(player, x, y)
