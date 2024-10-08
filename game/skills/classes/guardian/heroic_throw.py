from game.skills.types.entity_target_skill import EntityTargetSkill
from game.status_effects.debuffs.defense_debuff import DefenseDebuffStatusEffect


class HeroicThrow(EntityTargetSkill):
    """
    Throw your shield at an enemy dealing (85% attack damage).
    Generates high threat
    """

    def __init__(self, entity):
        super().__init__("Heroic Throw", 5, entity)

        self.active_time = 1
        self.casting_time = 1
        self.damage_factor = 1
        self.aggro_factor = 3
        self.effect_time = 10
        self.range = 16 * 4

        self.mana_gained = 1000

    def effect(self):
        self.single_target_attack()
