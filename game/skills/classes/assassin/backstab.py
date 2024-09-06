from game.skills.types.entity_target_skill import EntityTargetSkill


class Backstab(EntityTargetSkill):
    def __init__(self, entity):
        super().__init__("Backstab", 10, entity)

        self.active_time = 1
        self.casting_time = 1
        self.damage_factor = 2
        self.range = 16

    def effect(self):
        if not self.target:
            self.entity.idle()
            return

        self_prefix = "## Backstab\n\n"

        damage = self.damage_factor * self.entity.get_attack_damage()
        enemy = (self.target, damage, [], None)
        self.entity.deal_damage([enemy], self_prefix)
        self.target.interrupt()
