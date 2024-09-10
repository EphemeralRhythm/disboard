from game.skills.skill import Skill
from modules.combat import get_accessible_location
from game.command import Command


class LocationTargetSkill(Skill):
    def __init__(self, name, cooldown, entity):
        super().__init__(name, cooldown, entity)

        self.range = 15 * 16

    async def initialize(self, player, ctx, client, arg=None):
        loc = await get_accessible_location(
            client,
            ctx,
            player,
            "Enter the location that your want to teleport to",
            self.use_range,
        )

        if loc:
            self.x = loc[0]
            self.y = loc[1]

            return Command(name="cast", author=player, skill=self)

        return None
