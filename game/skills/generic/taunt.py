from game.skills.types.entity_target_skill import EntityTargetSkill


class Taunt(EntityTargetSkill):
    def __init__(self, entity):
        super().__init__("taunt", 10, entity)

        self.active_time = 1
        self.casting_time = 1

    def get_targets(self, client, player, x, y):
        return list(
            filter(
                lambda e: e.name != "player", super().get_targets(client, player, x, y)
            )
        )

    def effect(self):
        assert self.target, f"Skill {self} has no target"

        self.entity.notify(f"Used {self.name} on {self.target} gaining aggro.")

        aggro = max(self.target.aggro_table.values())

        self.target.aggro_table[self.entity] = aggro * 1.3
