from game.status_effects.status_effect import StatusEffect


class DEFBUffStatusEffect(StatusEffect):
    def __init__(self, entity, time, percent):
        super().__init__("def+", entity, time)
        self.remaining_time = time
        self.percent = percent

    def get_DEF_modifier(self) -> int:
        self.def_modifier = int(self.entity.DEF * self.percent / 100)
        return self.def_modifier
