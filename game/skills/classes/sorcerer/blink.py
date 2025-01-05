from game.skills.types.location_target_skill import LocationTargetSkill


class Blink(LocationTargetSkill):
    """ """

    def __init__(self, entity):
        super().__init__("Blink", 8, entity)

        self.active_time = 1
        self.casting_time = 1

        self.range = 16 * 12
        self.use_range = 16 * 12

        self.mana_required = 4000

    def effect(self):
        self.entity.x = self.x
        self.entity.y = self.y

        self.entity.notify("# Blink\nUsed blink to teleport to the specified location.")
