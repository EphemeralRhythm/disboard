from game.skills.types.inplace_skill import InplaceSkill
from game.status_effects.skills.stealth import StealthStatusEffect


class Vanish(InplaceSkill):
    """
    Allows you to vanish from sight, entering stealth while in combat.

    For the first 3 ticks after vanishing, damage and harmful effects received will not break stealth.
    Also breaks movement impairing effects.
    """

    def __init__(self, entity):
        super().__init__("Vanish", 12, entity)

        self.active_time = 1
        self.casting_time = 1
        self.effect_time = 600

        self.GENERATES_THREAT = False
        self.REMOVES_STEALTH = False
        self.IS_CRITABLE = False

    def effect(self):
        self.entity.status_effects = list(
            filter(lambda x: not x.IS_MOVEMENT_IMPAIRING, self.entity.status_effects)
        )

        self.entity.idle()
        e = StealthStatusEffect(self.entity, self.effect_time)
        e.immunity_period = 3
        self.entity.add_status_effect(e)
