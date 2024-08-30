class StatusEffect:
    def __init__(self, name, entity, remaining_time):
        self.name = name
        self.entity = entity
        self.remaining_time = remaining_time + 1

        self.silenced = False
        self.lock = False

    def update(self):
        """
        returns true is the status effect expired
        """

        self.remaining_time -= 1
        self.effect()
        return self.remaining_time > 0

    def effect(self):
        pass

    def get_DODGE_modifier(self) -> int:
        return 0

    def get_DEF_modifier(self) -> int:
        return 0

    def get_ATK_modifier(self) -> int:
        return 0

    def get_CRIT_modifier(self):
        return 0

    def OnTakeDamage(self):
        pass

    def renew(self, time):
        self.remaining_time = time
