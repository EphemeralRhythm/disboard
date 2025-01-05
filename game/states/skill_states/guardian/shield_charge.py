from typing import TYPE_CHECKING

from game.states.state import State
from game.states.entityStates.followState import follow

from utils.constants import COLOR_BLUE
from game.utils import distance

if TYPE_CHECKING:
    from game.entities.entity import Entity
    from game.skills.skill import Skill


class ShieldChargeState(State):
    def __init__(self, entity: "Entity", target: "Entity", timeout, skill: "Skill"):
        super().__init__(entity)

        self.name = "shield charge"
        self.action_name = "shield charge"
        self.time_remaining = timeout

        self.skill = skill
        self.target = target
        self.entity = entity

    def OnUpdate(self):
        self.time_remaining -= 1

        if self.time_remaining == 0:
            self.Exit()

        if not self.target:
            return

        target = self.target
        entity = self.entity

        if not target:
            return

        if distance(target, entity) > entity.attackRange:
            if not follow(entity, target, 3):
                return

        if distance(target, entity) > entity.attackRange:
            return

        boosted = ""
        if self.entity.has_active_skill("Shield Wall"):
            self.skill.damage_factor = 5
            boosted = "### **Shield Wall** boost!\n"

        attack = self.skill.init_primary_attack()

        notification = self.skill.prefix + self.entity.attack(self.target, attack)

        attack.damage = 1.3 * self.entity.get_attack_damage()

        targets = list(
            filter(
                lambda e: distance(self.entity, e) <= self.skill.impact_range * 16
                and e != self.target,
                self.skill.get_enemies(self.entity, 0, 0),
            )
        )

        for target in targets:
            notification += self.entity.attack(target, attack)

        self.entity.notify(notification, COLOR_BLUE)
        self.skill.deactivate()
        self.Exit()
