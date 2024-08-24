from game.skills.types.location_target_skill import LocationTargetSkill
from game.status_effects.skills.stealth import StealthStatusEffect


class GhostStep(LocationTargetSkill):
    def __init__(self, entity):
        super().__init__("Ghost Step", 10, entity)

        self.active_time = 4
        self.casting_time = 1

    def effect(self):
        if self.active_timeout == 4:
            e = StealthStatusEffect(self.entity, 3)
            self.entity.add_status_effect(e)

        if self.active_timeout == 1:
            self.entity.x = self.x
            self.entity.y = self.y
