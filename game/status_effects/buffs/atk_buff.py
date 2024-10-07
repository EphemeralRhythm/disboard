from game.status_effects.status_effect import StatusEffect


class ATKBUffStatusEffect(StatusEffect):
    def __init__(self, entity, time, percent):
        super().__init__("atk+", entity, time)
        self.remaining_time = time
        self.percent = percent

    def get_ATK_modifier(self) -> int:
        self.atk_modifier = int(self.entity.ATK * self.percent / 100)
        return self.atk_modifier
