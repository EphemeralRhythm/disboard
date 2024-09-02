from game.skills.types.inplace_skill import InplaceSkill
from game.utils import distance


class Shockwave(InplaceSkill):
    def __init__(self, entity):
        super().__init__("Shockwave", 10, entity)

        self.active_time = 1
        self.casting_time = 1
        self.impact_range = 3
        self.effect_time = 4

        self.damage = self.entity.get_attack_damage()

    def effect(self):
        enemies = self.entity.cell.get_targetable_entities(self.entity)
        targets = "Affected Targets:\n"

        for enemy in enemies:
            if distance(self.entity, enemy) <= self.impact_range * 16:
                enemy.get_stunned(self.effect_time)
                targets += f"- {enemy}: {self.damage}\n"

                enemy.take_damage(self.damage, self.entity)
                enemy.notify(
                    f"{self.entity} used shockwave dealing {self.damage} DAMAGE and stunning you for {self.effect_time} seconds."
                    + f"\nYour HP is now {enemy.HP}."
                )

        self.entity.notify("Using the skill **Shockwave**.\n" + targets)
