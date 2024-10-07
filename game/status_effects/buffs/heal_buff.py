from game.status_effects.status_effect import StatusEffect


class HealBuffStatusEffect(StatusEffect):
    def __init__(self, entity, time, percent):
        super().__init__("heal+", entity, time)
        self.remaining_time = time
        self.percent = percent

    def get_HEAL_modifier(self) -> int:
        self.heal_modifier = int(self.entity.HEAL * self.percent / 100)
        return self.heal_modifier
