from game.skills.types.entity_target_skill import EntityTargetSkill


class Fireball(EntityTargetSkill):
    def __init__(self, entity):
        super().__init__("Fireball", 10, entity)

        self.active_time = 1
        self.casting_time = 5

    def effect(self):
        assert self.target, f"Skill {self} has no target"
        self.target.take_damage_from_entity(self.entity, 30)
