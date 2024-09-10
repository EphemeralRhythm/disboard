from game.skills.types.entity_target_skill import EntityTargetSkill
from game.states.crowd_control_states.stunned_state import StunnedState


class ParalysisStrike(EntityTargetSkill):
    """
    A finishing move that consumes all your mana to stun the target for a duration of time.

    2000 mana ->  (2 ticks)
    4000 mana ->  (3 ticks)
    6000 mana ->  (4 ticks)
    8000 mana ->  (5 ticks)
    10000 mana -> (6 ticks)
    12000 mana -> (7 ticks)
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
        time = 2 + mana / 2000

        self.crowd_control_state = StunnedState(self.target, time)
        self.single_target_attack()
