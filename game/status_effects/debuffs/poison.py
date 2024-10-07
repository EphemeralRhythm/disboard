from game.status_effects.status_effect import StatusEffect
from utils.constants import COLOR_RED


class PoisonStatusEffect(StatusEffect):
    def __init__(self, entity, time, damage):
        super().__init__("poison", entity, time)
        self.remaining_time = time
        self.silenced = True
        self.damage = int(damage / time)

        self.IS_HARMFUL = True

    def effect(self):
        damage = self.entity.calculate_damage_dealt(self.damage)
        self.entity.HP -= damage

        notif = "## You took poison damage\n"
        notif += f"- **Damage Dealt:** {damage}\n"
        notif += f"- **HP Remaining:** {self.entity.HP}/{self.entity.MAX_HP}, ({int(self.entity.HP / self.entity.MAX_HP * 100)} %)\n"

        self.entity.on_take_damage()
        self.entity.notify(notif, COLOR_RED)

        if self.entity.HP <= 0:
            self.entity.die()
