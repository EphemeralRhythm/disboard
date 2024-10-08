from game.skills.types.location_target_skill import LocationTargetSkill


class ChampionsSpear(LocationTargetSkill):
    """
    Throw a spear a target location dealing (200% attack damage) for all enemies within 2 meter radius.
    """

    def __init__(self, entity):
        super().__init__("Champion's Spear", 13, entity)

        self.active_time = 1
        self.casting_time = 1
        self.damage_factor = 1
        self.range = 16 * 9
        self.impact_range = 5

        self.IS_INTERRUPT = True
        self.mana_gained = 1000

    def effect(self):
        self.multi_target_attack(self.x, self.y)
