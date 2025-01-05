from game.skills.types.inplace_skill import InplaceSkill
from game.states.skill_states.guardian.castle_in_stone import CastleInStoneState
from game.status_effects.specific.guardian.castle_in_stone import (
    CastleInStoneStatusEffect,
)


class CastleInStone(InplaceSkill):
    """ """

    def __init__(self, entity):
        super().__init__("Castle In Stone", 80, entity)

        self.active_time = 10
        self.casting_time = 1

        self.effect_time = 10

        self.mana_required = 6000

    def effect(self):
        if self.active_timeout == self.active_time:
            self.entity.notify("# Castle In Stone")

        self.entity.changeState(CastleInStoneState(self.entity, self.effect_time))
        self.entity.add_status_effect(
            CastleInStoneStatusEffect(self.entity, self.effect_time)
        )
