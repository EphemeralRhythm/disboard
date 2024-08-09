from game.skills.skill import Skill
from modules.combat import send_target_select
from game.command import Command


class EntityTargetSkill(Skill):
    def __init__(self, name, cooldown, entity):
        super().__init__(name, cooldown, entity)

    def get_targets(self, client, player):
        return client.world.get_targetable_entities(player)

    async def initialize(self, player, ctx, client):
        targets = self.get_targets(client, player)
        self.target = await send_target_select(
            client, targets, player, ctx, self.name.title()
        )

        if self.target:
            return Command(name="cast", author=player, skill=self)

        return None
