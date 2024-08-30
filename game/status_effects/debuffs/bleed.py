from game.status_effects.status_effect import StatusEffect


class BleedStatusEffect(StatusEffect):
    def __init__(self, entity, time):
        super().__init__("bleed", entity, time)
        self.remaining_time = time

    def effect(self):
        pass
