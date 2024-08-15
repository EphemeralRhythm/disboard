from game.skills.types.entity_target_skill import EntityTargetSkill


class ShieldBash(EntityTargetSkill):
    def __init__(self, entity):
        super().__init__("Shield Bash", 5, entity)

        self.active_time = 1
        self.casting_time = 1
        self.damage = 10

    def effect(self):
        assert self.target, f"Skill {self} has no target"
        self.target.take_damage(self.damage, self.entity)
        self.entity.notify(
            f"Attacked {self.target} with a shield bash dealing {self.damage} damage and stunning the enemy."
        )
        self.target.get_stunned(5)
