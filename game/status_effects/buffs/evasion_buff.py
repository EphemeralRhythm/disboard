from game.status_effects.status_effect import StatusEffect


class EvasionBuffStatusEffect(StatusEffect):
    def __init__(self, entity, time, percent):
        super().__init__("evasion+", entity, time)
        self.remaining_time = time
        self.percent = percent

    def get_DODGE_modifier(self):
        self.evasion_modifier = int(self.entity.DODGE * self.percent / 100)
        return self.evasion_modifier
