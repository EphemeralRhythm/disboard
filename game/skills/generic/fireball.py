from game.skills.types.entity_target_skill import EntityTargetSkill


class Fireball(EntityTargetSkill):
    def __init__(self, entity):
        super().__init__("Fireball", 10, entity)

        self.active_time = 1
        self.casting_time = 5
        self.damage = 30

    def effect(self):
        assert self.target, f"Skill {self} has no target"
        self.target.take_damage(self.damage, self.entity)
        self.entity.notify(
            f"Attacked {self.target} with a fireball dealing {self.damage} damage."
        )
