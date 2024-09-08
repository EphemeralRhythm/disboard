from game.status_effects.status_effect import StatusEffect


class StealthStatusEffect(StatusEffect):
    def __init__(self, entity, time):
        super().__init__("stealth", entity, time)
        self.remaining_time = time
        self.immunity_period = 0

    def effect(self):
        if self.immunity_period > 0:
            self.immunity_period -= 1

    def OnTakeDamage(self):
        if self.immunity_period <= 0:
            self.entity.remove_stealth()
