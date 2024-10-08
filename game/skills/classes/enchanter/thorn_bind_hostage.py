from game.skills.types.entity_target_skill import EntityTargetSkill
from game.status_effects.specific.enchanter.thorn_bind_hostage import (
    ThornBindHostageStatusEffect,
)


class ThornBindHostage(EntityTargetSkill):
    """
    Encircle your target with thorns that deal damage when destroyed by a melee attack.
    """

    def __init__(self, entity):
        super().__init__("Thorn Bind Hostage", 15, entity)

        self.active_time = 1
        self.casting_time = 1
        self.damage_factor = 0
        self.effect_time = 8
        self.range = 16 * 4

    def effect(self):
        self.status_effects = [
            ThornBindHostageStatusEffect(
                self.target, int(self.entity.get_attack_damage() * 1.2)
            )
        ]

        self.single_target_attack()
