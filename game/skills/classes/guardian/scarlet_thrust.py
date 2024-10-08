from game.skills.types.entity_target_skill import EntityTargetSkill
from utils.constants import COLOR_BLUE


class ScarletThrust(EntityTargetSkill):
    """ """

    def __init__(self, entity):
        super().__init__("Scarlet Thrust", 15, entity)

        self.active_time = 1
        self.casting_time = 1
        self.damage_factor = 1.2
        self.range = 16

        self.mana_gained = 1000

    def effect(self):
        if not self.target:
            self.entity.idle()
            return

        attack = self.init_primary_attack()
        notification = self.prefix + self.entity.attack(self.target, attack)

        if self.mana_gained != 0:
            notification += self.notify_mana()

        regenerated_hp = min(
            int(0.2 * self.entity.MAX_HP), self.entity.MAX_HP - self.entity.HP
        )
        self.entity.heal(regenerated_hp)

        notification += "\n## Regeneration\n"
        notification += f"- Regenerated HP: {regenerated_hp}\n"
        notification += f"- HP: {self.entity.HP}"

        self.entity.notify(notification, COLOR_BLUE)
