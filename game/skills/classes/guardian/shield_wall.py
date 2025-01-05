from game.skills.types.inplace_skill import InplaceSkill
from game.status_effects.buffs.def_buff import DEFBUffStatusEffect


class ShieldWall(InplaceSkill):
    """
    Raise your shield boosting your DEF by 150% for 4 ticks.
    Has a 50% chance to remove the cooldown on your next Shield Charge.
    """

    def __init__(self, entity):
        super().__init__("Shield Wall", 15, entity)

        self.active_time = 10
        self.casting_time = 1
        self.effect_time = 4

    def effect(self):
        if self.active_timeout == self.active_time:
            self.entity.add_status_effect(
                DEFBUffStatusEffect(self.entity, self.effect_time, 150)
            )
