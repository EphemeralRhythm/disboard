from game.status_effects.status_effect import StatusEffect


class BlindStatusEffect(StatusEffect):
    def __init__(self, entity, time):
        super().__init__("blind", entity, time)
        self.remaining_time = time

    def effect(self):
        pass
