from game.skills.types.inplace_skill import InplaceSkill

from game.utils import distance


class DeathSweep(InplaceSkill):
    def __init__(self, entity):
        super().__init__("Death Sweep", 10, entity)

        self.active_time = 1
        self.casting_time = 1
        self.impact_range = 2

        self.damage = self.entity.get_attack_damage()

    def effect(self):
        enemies = self.entity.cell.get_targetable_entities(self.entity)

        targets = "Affected Targets:\n"

        for enemy in enemies:
            if distance(self.entity, enemy) <= self.impact_range * 16:
                targets += f"- {enemy}: {self.damage}\n"

                enemy.take_damage(self.damage, self.entity)
                enemy.notify(
                    f"{self.entity} attacked you using the skill Death Sweep dealing {self.damage} DAMAGE.\nYour HP is now {enemy.HP}"
                )

        self.entity.notify("Using the skill **Death Sweep**.\n" + targets)
