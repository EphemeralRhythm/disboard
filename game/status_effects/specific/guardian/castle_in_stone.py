from game.status_effects.status_effect import StatusEffect


class CastleInStoneStatusEffect(StatusEffect):
    def __init__(self, entity, time):
        super().__init__("Castle In Stone", entity, time)
        self.remaining_time = time

    def get_DEF_modifier(self) -> int:
        return int(1e6)
