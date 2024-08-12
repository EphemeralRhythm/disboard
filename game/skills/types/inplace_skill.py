from game.skills.skill import Skill
from game.command import Command


class InplaceSkill(Skill):
    def __init__(self, name, cooldown, entity):
        super().__init__(name, cooldown, entity)

    async def initialize(self, player, ctx, client) -> Command | None:
        return Command(name="cast", author=player, skill=self)
