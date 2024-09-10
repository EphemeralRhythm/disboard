from game.skills.types.entity_target_skill import EntityTargetSkill
from game.states.crowd_control_states.disoriented_state import DisorientedState


class Blind(EntityTargetSkill):
    """
    Blind all the enemies around you for 8 seconds.
    """

    def __init__(self, entity):
        super().__init__("Blind", 30, entity)

        self.active_time = 1
        self.casting_time = 1
        self.damage_factor = 0
        self.impact_range = 3
        self.range = 16
        self.crowd_control_state = DisorientedState(None, 8)

    def effect(self):
        self.multi_target_attack()
