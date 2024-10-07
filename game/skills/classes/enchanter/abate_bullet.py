from game.skills.types.entity_target_skill import EntityTargetSkill
from game.status_effects.debuffs.defense_debuff import DefenseDebuffStatusEffect


class AbateBullet(EntityTargetSkill):
    """
    An attack that deals a small amount of damage to an enemy and lowers their defense.
    """

    def __init__(self, entity):
        super().__init__("Abate Bullet", 5, entity)

        self.active_time = 1
        self.casting_time = 1
        self.damage_factor = 1
        self.effect_time = 10
        self.range = 16 * 4

        self.mana_gained = 1000

    def effect(self):
        self.status_effects = [
            DefenseDebuffStatusEffect(self.target, self.effect_time, 5)
        ]

        self.single_target_attack()
