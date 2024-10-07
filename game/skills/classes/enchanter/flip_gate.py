from game.skills.types.entity_target_skill import EntityTargetSkill


class FlipGate(EntityTargetSkill):
    """ """

    def __init__(self, entity):
        super().__init__("Flip Gate", 20, entity)

        self.active_time = 1
        self.casting_time = 1
        self.damage_factor = 0
        self.effect_time = 10
        self.range = 16

    def effect(self):
        pass
