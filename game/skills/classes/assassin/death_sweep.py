from game.skills.types.inplace_skill import InplaceSkill

from game.utils import distance


class DeathSweep(InplaceSkill):
    def __init__(self, entity):
        super().__init__("Death Sweep", 10, entity)

        self.active_time = 1
        self.casting_time = 1
        self.impact_range = 3

        self.damage_factor = 1

    def effect(self):
        damage = self.damage_factor * self.entity.get_attack_damage()

        enemies = self.entity.cell.get_targetable_entities(self.entity)
        targets = []

        self_prefix = "## Death Sweep\n\n"
        for enemy in enemies:
            if distance(self.entity, enemy) <= self.impact_range * 16:
                targets.append((enemy, damage, [], None))

        self.entity.deal_damage(targets, self_prefix)
