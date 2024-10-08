from game.skills.types.inplace_skill import InplaceSkill
from game.status_effects.buffs.def_buff import DEFBUffStatusEffect


class ShieldWall(InplaceSkill):
    """ """

    def __init__(self, entity):
        super().__init__("Shield Wall", 15, entity)

        self.active_time = 1
        self.casting_time = 1
        self.effect_time = 8

    def effect(self):
        self.entity.add_status_effect(
            DEFBUffStatusEffect(self.target, self.effect_time, 150)
        )
