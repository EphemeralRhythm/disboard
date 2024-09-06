from game.skills.types.entity_target_skill import EntityTargetSkill


class Assassinate(EntityTargetSkill):
    def __init__(self, entity):
        super().__init__("Assassinate", 20, entity)

        self.active_time = 1
        self.casting_time = 1
        self.damage_factor = 4
        self.range = 16

    def effect(self):
        self.single_target_attack()
