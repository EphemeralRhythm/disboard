from game.skills.types.entity_target_skill import EntityTargetSkill
from game.states.crowd_control_states.sleep_state import SleepState


class Shadowbind(EntityTargetSkill):
    """
    A crowd control ability that incapacitates an enemy not in combat for a long duration.
    """

    def __init__(self, entity):
        super().__init__("Shadowbind", 10, entity)

        self.active_time = 1
        self.casting_time = 1
        self.damage_factor = 0
        self.range = 16

        self.REQUIRES_STEALTH = True
        self.REQUIRES_TARGET_OUT_OF_COMBAT = True

    def effect(self):
        self.crowd_control_state = SleepState(self.target, 5)
        self.single_target_attack()
