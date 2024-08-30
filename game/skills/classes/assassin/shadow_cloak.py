from game.skills.types.inplace_skill import InplaceSkill
from game.status_effects.skills.stealth import StealthStatusEffect


class ShadowCloak(InplaceSkill):
    def __init__(self, entity):
        super().__init__("Shadow Cloak", 10, entity)

        self.active_time = 1
        self.casting_time = 1
        self.ALLOW_IN_COMBAT = False

    def effect(self):
        e = StealthStatusEffect(self.entity, 600)
        self.entity.add_status_effect(e)
        self.entity.notify("Activated the skill Shadow Cloak. You are invisible now.")
