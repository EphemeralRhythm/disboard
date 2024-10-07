from game.skills.types.entity_target_skill import EntityTargetSkill


class RapidCut(EntityTargetSkill):
    """
    Swiftly cut your target, dealing (0.7 attack damage) and generating 4000 mana.
    """

    def __init__(self, entity):
        super().__init__("Rapid Cut", 10, entity)

        self.active_time = 1
        self.casting_time = 1
        self.damage_factor = 0.7
        self.range = 16

        self.mana_gained = 4000
        self.IS_INTERRUPT = True

    def effect(self):
        self.single_target_attack()
