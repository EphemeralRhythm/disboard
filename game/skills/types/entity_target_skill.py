from game.skills.skill import Skill


class EntityTargetSkill(Skill):
    def __init__(self, name, cooldown, entity):
        super().__init__(name, cooldown, entity)

    def initialize(self, player, ctx, client):
