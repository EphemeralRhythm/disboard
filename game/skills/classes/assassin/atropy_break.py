from game.skills.types.entity_target_skill import EntityTargetSkill


class AtrophyBreak(EntityTargetSkill):
    def __init__(self, entity):
        super().__init__("Atrophy Break", 10, entity)

        self.active_time = 1
        self.casting_time = 1
        self.damage = self.entity.get_attack_damage()

        self.stun_time = 3
        self.range = 5 * 16

    def effect(self):
        assert self.target, f"Skill {self} has no target"

        self.entity.notify(
            f"Attacked {self.target} with Atrophy Break {self.damage} damage and stunning the enemy for {self.stun_time} ticks."
        )
        self.target.take_damage(self.damage, self.entity)
        self.target.get_stunned(self.stun_time)
