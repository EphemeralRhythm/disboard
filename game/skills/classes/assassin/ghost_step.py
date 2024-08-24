from game.skills.types.location_target_skill import LocationTargetSkill
from game.status_effects.skills.stealth import StealthStatusEffect


class GhostStep(LocationTargetSkill):
    def __init__(self, entity):
        super().__init__("Ghost Step", 10, entity)

        self.active_time = 3
        self.casting_time = 1
        self.use_range = 7

    def effect(self):
        if self.active_timeout == 3:
            e = StealthStatusEffect(self.entity, 2)
            self.entity.add_status_effect(e)
            self.entity.notify(
                "Activating the skill **Ghost Step**. You are now invisible."
            )

        if self.active_timeout == 1:
            self.entity.x = self.x
            self.entity.y = self.y
            self.entity.notify(
                "Used the skill **Ghost Step** to teleport to the specified location. You are no longer invisble."
            )
