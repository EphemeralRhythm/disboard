from game.status_effects.status_effect import StatusEffect


class EvasionBuffStatusEffect(StatusEffect):
    def __init__(self, entity, time, percent):
        super().__init__("evasion+", entity, time)
        self.remaining_time = time

        self.evasion_modifier = int(self.entity.DODGE * percent / 100)

    def get_DODGE_modifier(self):
        return self.evasion_modifier
