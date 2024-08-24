from game.skills.types.inplace_skill import InplaceSkill
from game.utils import distance


class SmokeScreen(InplaceSkill):
    def __init__(self, entity):
        super().__init__("Smoke Screen", 10, entity)

        self.active_time = 1
        self.casting_time = 1
        self.impact_range = 2

    def effect(self):
        enemies = self.entity.cell.get_targetable_entities(self.entity)
        targets = "Affected Targets:\n"

        for enemy in enemies:
            if distance(self.entity, enemy) <= self.impact_range * 16:
                enemy.get_stunned(2)
                targets += f"- {enemy}\n"

                enemy.notify(
                    f"{self.entity} used smoke screen stunning you for 2 ticks."
                )

        self.entity.notify("Using the skill **Smoke Screen**.\n" + targets)
