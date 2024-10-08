from game.status_effects.status_effect import StatusEffect
from utils.constants import COLOR_RED


class ThornBindHostageStatusEffect(StatusEffect):
    def __init__(self, entity, damage):
        super().__init__("Thorn Bind Hostage", entity, 5)

        self.remaining_time = 24
        self.damage_factor = 0
        self.damage = damage
        self.MAX_STACKS = 4

        self.IS_HARMFUL = True

    def effect(self):
        pass

    def OnTakeDamage(self):
        damage = self.entity.calculate_damage_dealt(self.damage) * self.stacks
        self.entity.HP -= damage

        notif = "# Thorns Broken\n"
        notif += f"You took damage from {self.stacks} {'stack' if self.stacks == 1 else 'stacks'} of thorn bind hostage.\n"
        notif += f"- **Damage Dealt:** {damage}\n"
        notif += f"- **HP Remaining:** {self.entity.HP}/{self.entity.MAX_HP}, ({int(self.entity.HP / self.entity.MAX_HP * 100)} %)\n"

        self.entity.on_take_damage()
        self.entity.notify(notif, COLOR_RED)

        if self.entity.HP <= 0:
            self.entity.die()

        self.entity.status_effects.remove(self)
