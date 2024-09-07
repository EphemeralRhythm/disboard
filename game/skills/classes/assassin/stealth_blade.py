from game.skills.types.entity_target_skill import EntityTargetSkill
from game.states.crowd_control_states.stunned_state import StunnedState


class StealthBlade(EntityTargetSkill):
    """
    Strike your target from the shadows dealing damage and inflicting stun for a short period.
    """

    def __init__(self, entity):
        super().__init__("Stealth Blade", 10, entity)

        self.active_time = 1
        self.casting_time = 1
        self.effect_time = 4
        self.damage_factor = 1.4
        self.range = 16

        self.REQUIRES_STEALTH = True

    def effect(self):
        self.crowd_control_state = StunnedState(self.target, self.effect_time)
        self.single_target_attack()
