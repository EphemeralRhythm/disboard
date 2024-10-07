from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.entities.entity import Entity


class StatusEffect:
    def __init__(self, name, entity: "Entity", remaining_time):
        self.name = name
        self.entity = entity
        self.remaining_time = remaining_time + 1

        self.silenced = False
        self.lock = False

        self.IS_HARMFUL = False
        self.IS_MOVEMENT_IMPAIRING = False

        self.stacks = 1
        self.MAX_STACKS = 1

    def update(self):
        """
        returns true is the status effect expired
        """

        self.remaining_time -= 1
        self.effect()
        return self.remaining_time > 0

    def __repr__(self) -> str:
        return f"{self.name} - ({self.remaining_time})"

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, StatusEffect):
            return False

        return self.name == __value.name

    def effect(self):
        pass

    def get_DODGE_modifier(self) -> int:
        return 0

    def get_DEF_modifier(self) -> int:
        return 0

    def get_ATK_modifier(self) -> int:
        return 0

    def get_HEAL_modifier(self) -> int:
        return 0

    def get_CRIT_modifier(self) -> int:
        return 0

    def get_ACC_modifier(self) -> int:
        return 0

    def get_aggro_modifier(self) -> int:
        return 1

    def OnTakeDamage(self):
        pass

    def renew(self, time):
        self.remaining_time = time

        if not self.stacks == self.MAX_STACKS:
            self.stacks += 1
