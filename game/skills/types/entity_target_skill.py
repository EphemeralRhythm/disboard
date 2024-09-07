from typing_extensions import List
from game.skills.skill import Skill
from modules.combat import send_target_select, get_location
from game.command import Command

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.entities.entity import Entity


class EntityTargetSkill(Skill):
    def __init__(self, name, cooldown, entity):
        super().__init__(name, cooldown, entity)
        self.REQUIRES_TARGET = True

    def get_targets(self, client, player, x, y) -> List["Entity"]:
        return client.world.get_targetable_entities(player, x, y)

    async def initialize(self, player, ctx, client):
        loc = await get_location(
            client, ctx, player, "Enter the location of your target.", self.use_range
        )

        if not loc:
            return None

        x, y = loc

        targets = self.get_targets(client, player, x, y)

        self.target = await send_target_select(
            client, targets, player, ctx, self.name.title()
        )

        if self.target:
            if self.REQUIRES_TARGET_OUT_OF_COMBAT and self.target.is_in_combat():
                await ctx.send("This skill requires target to be out of combat.")
                return None

            return Command(name="cast", author=player, skill=self)

        return None
