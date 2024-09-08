from game.utils import distance
from game.skills.types.entity_target_skill import EntityTargetSkill


class FanOfKnives(EntityTargetSkill):
    """
    Sprays knives at all enemies within 8 meters, dealing (80% attack damage).
    """

    def __init__(self, entity):
        super().__init__("Fan Of Knives", 15, entity)

        self.active_time = 1
        self.casting_time = 1
        self.damage_factor = 0.8
        self.impact_range = 8
        self.range = 16

        self.mana_gained = 2000

    def effect(self):
        self.multi_target_attack()
