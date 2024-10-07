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
        return super().get_enemies(client, player, x, y)

    async def initialize(self, player, ctx, client, arg=None):

        if not arg:
            loc = await get_location(
                client,
                ctx,
                player,
                "Enter the location of your target.",
                self.use_range,
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

        elif arg == "c":
            if not player.stateManager.currentState.name == "attack":
                await ctx.send("No target found.")
                return None

            self.target = player.stateManager.currentState.target
            return Command(name="cast", author=player, skill=self)

        elif arg == "n":
            targets = self.get_targets(client, player, 0, 0)

            if not targets:
                await ctx.send("No target found.")
                return None

            self.target = targets[0]
            return Command(name="cast", author=player, skill=self)

        return None
