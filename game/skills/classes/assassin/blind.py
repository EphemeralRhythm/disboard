from game.skills.types.entity_target_skill import EntityTargetSkill


class Blind(EntityTargetSkill):
    def __init__(self, entity):
        super().__init__("Blind", 10, entity)

        self.active_time = 1
        self.casting_time = 1

        self.blind_time = 6
        self.range = 16

    def effect(self):
        assert self.target, f"Skill {self} has no target"

        self.entity.notify(
            f"Used Blind on {self.target}.\nThe target is now blind for {self.blind_time} ticks."
        )

        self.target.notify(
            f"{self.entity} used the skill Blind disorienting you for {self.blind_time} ticks."
        )
        self.target.get_disoriented(self.blind_time)
