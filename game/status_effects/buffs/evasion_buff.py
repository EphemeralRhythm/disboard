from game.status_effects.status_effect import StatusEffect


class EvasionBuffStatusEffect(StatusEffect):
    def __init__(self, entity, time):
        super().__init__("evasion+", entity, time)
        self.remaining_time = time

        self.evasion_modifier = self.entity.DODGE * 0.4

    def get_DODGE_modifier(self):
        return self.evasion_modifier
