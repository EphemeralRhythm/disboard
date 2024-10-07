from typing import TYPE_CHECKING, List

from game.skills.types.entity_target_skill import EntityTargetSkill
from game.status_effects.buffs.atk_buff import ATKBUffStatusEffect

if TYPE_CHECKING:
    from game.entities.entity import Entity


class KeenEdge(EntityTargetSkill):
    """
    Boosts an ally's attack damage by 30% for 10 ticks.
    """

    def __init__(self, entity):
        super().__init__("Keen Edge", 20, entity)

        self.active_time = 1
        self.casting_time = 1
        self.damage_factor = 0
        self.effect_time = 10
        self.range = 4 * 16

    def get_targets(self, client, player, x, y) -> List["Entity"]:
        return client.world.get_allied_entities(player, x, y)

    def effect(self):
        if not self.target:
            self.entity.idle()
            return

        self.target.add_status_effect(
            ATKBUffStatusEffect(self.target, self.effect_time, 30)
        )
