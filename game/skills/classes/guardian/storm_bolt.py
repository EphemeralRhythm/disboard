from game.skills.types.entity_target_skill import EntityTargetSkill


class StormBolt(EntityTargetSkill):
    """ """

    def __init__(self, entity):
        super().__init__("Storm Bolt", 10, entity)

        self.active_time = 1
        self.casting_time = 1
        self.damage_factor = 1
        self.range = 16

        self.mana_gained = 4000
        self.IS_INTERRUPT = True

    def effect(self):
        self.single_target_attack()
