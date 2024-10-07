from typing import TYPE_CHECKING, List

from game.skills.types.entity_target_skill import EntityTargetSkill
from game.status_effects.buffs.atk_buff import ATKBUffStatusEffect

if TYPE_CHECKING:
    from game.entities.entity import Entity


class ForceStep(EntityTargetSkill):
    """
    Reduce the cooldown timeout for all non active skills for an ally by 5 ticks.
    """

    def __init__(self, entity):
        super().__init__("Force Step", 20, entity)

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

        for skill in self.target.skills:
            if not skill.active and not skill.casting:
                skill.cooldown_timeout -= 5
                skill.cooldown_timeout = max(0, skill.cooldown_timeout)
