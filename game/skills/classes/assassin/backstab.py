from game.skills.types.entity_target_skill import EntityTargetSkill


class Backstab(EntityTargetSkill):
    def __init__(self, entity):
        super().__init__("Backstab", 10, entity)

        self.active_time = 1
        self.casting_time = 1
        self.damage = 2 * self.entity.get_attack_damage()
        self.range = 16

    def effect(self):
        assert self.target, f"Skill {self} has no target"

        self.target.take_damage(self.damage, self.entity)

        self.entity.notify(
            f"Attacked {self.target} with the skill Backstab dealing {self.damage} damage."
            + f"\nEnemy HP is now {self.target.HP}"
        )
