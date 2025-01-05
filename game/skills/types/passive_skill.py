from game.skills.skill import Skill
from game.command import Command


class PassiveSkill(Skill):
    def __init__(self, name, cooldown, entity):
        super().__init__(name, cooldown, entity)

    async def initialize(self, player, ctx, client, arg=None) -> Command | None:
        await ctx.send("This is a passive skill.")
        return None
