from game.skills.types.entity_target_skill import EntityTargetSkill
from game.status_effects.generic.damage_over_time import DamageOverTimeStatusEffect


class ElectricFuzz(EntityTargetSkill):
    """
    A lightning element attack that deals (500% attack damage) over 10 ticks.
    """

    def __init__(self, entity):
        super().__init__("Electric Fuzz", 15, entity)

        self.active_time = 1
        self.casting_time = 3
        self.damage_factor = 0
        self.range = 16 * 4

        self.effect_time = 10

    def effect(self):
        self.status_effects = [
            DamageOverTimeStatusEffect(
                "Electric Fuzz",
                self.target,
                self.effect_time,
                5 * self.entity.get_attack_damage(),
            )
        ]

        self.single_target_attack()
