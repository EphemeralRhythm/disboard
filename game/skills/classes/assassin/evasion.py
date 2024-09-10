from game.skills.types.inplace_skill import InplaceSkill
from game.status_effects.buffs.evasion_buff import EvasionBuffStatusEffect


class Evasion(InplaceSkill):
    """
    Increase your dodge chance by 100% for 8 ticks.
    """

    def __init__(self, entity):
        super().__init__("Evasion", 40, entity)

        self.active_time = 1
        self.casting_time = 1
        self.effect_time = 8

        self.GENERATES_THREAT = False
        self.REMOVES_STEALTH = False
        self.IS_CRITABLE = False

    def effect(self):
        e = EvasionBuffStatusEffect(self.entity, self.effect_time, 100)
        self.entity.add_status_effect(e)
