from game.skills.types.entity_target_skill import EntityTargetSkill
from game.states.crowd_control_states.stunned_state import StunnedState


class ParalysisStrike(EntityTargetSkill):
    """
    A finishing move that consumes all your mana to stun the target for a duration of time. The length of the duration is affected by the amount of mana spent.
    """

    def __init__(self, entity):
        super().__init__("Paralysis Strike", 10, entity)

        self.active_time = 1
        self.casting_time = 1
        self.damage_factor = 1
        self.range = 16
        self.mana_required = 2000

    def effect(self):
        mana = self.entity.MP
        time = 3 + mana / 2000

        self.crowd_control_state = StunnedState(self.target, time)
        self.single_target_attack()
