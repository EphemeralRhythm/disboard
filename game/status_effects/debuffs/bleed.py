from game.status_effects.status_effect import StatusEffect
from utils.constants import COLOR_RED


class BleedStatusEffect(StatusEffect):
    def __init__(self, entity, time, damage):
        super().__init__("bleed", entity, time)
        self.remaining_time = time
        self.silenced = True
        self.damage = int(damage / time)

        self.IS_HARMFUL = True

    def effect(self):
        damage = self.entity.calculate_damage_dealt(self.damage)
        self.entity.HP -= damage

        notif = "## You took bleeding damage\n"
        notif += f"- **Damage Dealt:** {damage}\n"
        notif += f"- **HP Remaining:** {self.entity.HP}/{self.entity.MAX_HP}, ({int(self.entity.HP / self.entity.MAX_HP * 100)} %)\n"

        self.entity.on_take_damage()
        self.entity.notify(notif, COLOR_RED)

        if self.entity.HP <= 0:
            self.entity.die()
