from game.skills.types.entity_target_skill import EntityTargetSkill
from game.status_effects.debuffs.bleed import BleedStatusEffect


class GrimSlash(EntityTargetSkill):
    """
    Slash through the enemy dealing (310% attack damage) bleed damage over 6 ticks.
    """

    def __init__(self, entity):
        super().__init__("Grim Slash", 10, entity)

        self.active_time = 1
        self.casting_time = 1
        self.effect_time = 6
        self.damage_factor = 0.3
        self.range = 16

        self.mana_gained = 2000

    def effect(self):
        self.status_effects = [
            BleedStatusEffect(
                self.target,
                self.effect_time,
                3.1 * self.entity.get_attack_damage(),
            )
        ]

        self.single_target_attack()
