from game.skills.types.entity_target_skill import EntityTargetSkill


class Assassinate(EntityTargetSkill):
    def __init__(self, entity):
        super().__init__("Assassinate", 20, entity)

        self.active_time = 1
        self.casting_time = 1
        self.damage = 4 * self.entity.get_attack_damage()
        self.range = 16

    def effect(self):
        assert self.target, f"Skill {self} has no target"

        self.target.take_damage(self.damage, self.entity)

        self.entity.notify(
            f"Attacked {self.target} with the skill Assassinate dealing {self.damage} damage."
            + f"\nEnemy HP is now {self.target.HP}"
        )

        self.target.notify(
            f"{self.entity} attacked you using the skill Assassinate dealing {self.damage} DAMAGE."
            + f"\nHP is now {self.target.HP}."
        )
