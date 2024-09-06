from game.skills.types.entity_target_skill import EntityTargetSkill
from game.states.crowd_control_states.disoriented_state import DisorientedState


class AtrophyBreak(EntityTargetSkill):
    def __init__(self, entity):
        super().__init__("Atrophy Break", 10, entity)

        self.active_time = 1
        self.casting_time = 1
        self.damage_factor = 1

        self.effect_time = 8
        self.range = 5 * 16

    def effect(self):
        if not self.target:
            self.entity.idle()
            return

        self_prefix = "## Atrophy Break\n\n"

        damage = self.damage_factor * self.entity.get_attack_damage()
        enemy = (
            self.target,
            damage,
            [],
            DisorientedState(self.target, self.effect_time),
        )
        self.entity.deal_damage([enemy], self_prefix)
