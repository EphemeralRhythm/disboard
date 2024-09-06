from game.skills.types.entity_target_skill import EntityTargetSkill


class Blind(EntityTargetSkill):
    def __init__(self, entity):
        super().__init__("Blind", 10, entity)

        self.active_time = 1
        self.casting_time = 1

        self.blind_time = 6
        self.range = 16

    def effect(self):
        if not self.target:
            self.entity.idle()
            return

        self_prefix = "## Blind\n\n"

        damage = self.damage_factor * self.entity.get_attack_damage()
        enemy = (self.target, damage, [], None)
        self.entity.deal_damage([enemy], self_prefix)
        self.target.interrupt()
