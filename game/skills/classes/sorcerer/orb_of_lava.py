from game.skills.types.entity_target_skill import EntityTargetSkill


class OrbOfLava(EntityTargetSkill):
    """ """

    def __init__(self, entity):
        super().__init__("Orb Of Lava", 1, entity)

        self.active_time = 1
        self.casting_time = 4
        self.damage_factor = 6
        self.range = 16 * 6

        self.mana_gained = 2000
        self.IS_INTERRUPT = True

    def effect(self):
        self.single_target_attack()
