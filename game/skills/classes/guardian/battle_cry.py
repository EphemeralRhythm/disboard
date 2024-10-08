from game.skills.types.inplace_skill import InplaceSkill
from game.status_effects.buffs.def_buff import DEFBUffStatusEffect


class BattleCry(InplaceSkill):
    """
    Let out a powerful roar that increases the DEF of your allies within 12 meters by 200% for 8 ticks.
    """

    def __init__(self, entity):
        super().__init__("Battle Cry", 15, entity)

        self.active_time = 1
        self.casting_time = 1
        self.impact_range = 12
        self.effect_time = 8

    def effect(self):
        self.status_effects = [DEFBUffStatusEffect(self.target, self.effect_time, 200)]
        self.multi_target_support()
