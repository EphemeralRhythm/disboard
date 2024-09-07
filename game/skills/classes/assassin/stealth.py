from game.skills.types.inplace_skill import InplaceSkill
from game.status_effects.skills.stealth import StealthStatusEffect


class Stealth(InplaceSkill):
    """
    Conceals you in the shadows, allowing you to stalk enemies wihtout being seen.
    """

    def __init__(self, entity):
        super().__init__("Stealth", 1, entity)

        self.active_time = 1
        self.casting_time = 1
        self.effect_time = 600

        self.ALLOW_WHILE_STEALTHED = True
        self.REQUIRES_OUT_OF_COMBAT = True

    def effect(self):
        e = StealthStatusEffect(self.entity, self.effect_time)
        self.entity.add_status_effect(e)
