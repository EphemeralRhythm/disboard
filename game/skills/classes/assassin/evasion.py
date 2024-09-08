from game.skills.types.inplace_skill import InplaceSkill
from game.status_effects.buffs.evasion_buff import EvasionBuffStatusEffect


class Evasion(InplaceSkill):
    def __init__(self, entity):
        super().__init__("Evasion", 30, entity)

        self.active_time = 1
        self.casting_time = 1

    def effect(self):
        e = EvasionBuffStatusEffect(self.entity, 10, 100)
        self.entity.add_status_effect(e)
