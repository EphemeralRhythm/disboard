from game.skills.types.inplace_skill import InplaceSkill
from game.utils import distance


class SmokeScreen(InplaceSkill):
    def __init__(self, entity):
        super().__init__("Smoke Screen", 10, entity)

        self.active_time = 1
        self.casting_time = 1
        self.impact_range = 2
        self.damage = self.entity.get_attack_damage()

    def effect(self):
        self.entity.notify("Using the skill Smoke Screen.")
        enemies = self.entity.cell.get_targetable_entities(self.entity)

        for enemy in enemies:
            if distance(self.entity, enemy) <= self.impact_range * 16:
                enemy.take_damage(self.damage, self.entity)
                enemy.get_stunned(2)
