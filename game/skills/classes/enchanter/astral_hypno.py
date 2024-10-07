from game.skills.types.entity_target_skill import EntityTargetSkill
from game.states.crowd_control_states.sleep_state import SleepState


class AstralHypno(EntityTargetSkill):
    """
    A crowd control ability that neutralizes an enemy making them fall asleep.
    """

    def __init__(self, entity):
        super().__init__("Astral Hypno", 15, entity)

        self.active_time = 1
        self.casting_time = 1
        self.damage_factor = 0
        self.effect_time = 8
        self.range = 16 * 4

    def effect(self):
        self.crowd_control_state = SleepState(self.target, self.effect_time)
        self.single_target_attack()
