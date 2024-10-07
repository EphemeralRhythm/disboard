from game.skills.types.entity_target_skill import EntityTargetSkill
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from game.entities.entity import Entity


class ManaSiphon(EntityTargetSkill):
    """
    Depletes your entire mana to give mana to another player. Maximum mana transferred is 4000.
    """

    def __init__(self, entity):
        super().__init__("Mana Siphon", 20, entity)

        self.active_time = 1
        self.casting_time = 1
        self.damage_factor = 0
        self.effect_time = 10
        self.range = 16

    def get_targets(self, client, player, x, y) -> List["Entity"]:
        return self.get_allies(client, player, x, y)

    def effect(self):
        if not self.target:
            self.entity.idle()
            return

        amount = min(self.entity.MP, self.target.MAX_MP - self.target.MP, 4000)

        self.entity.lose_MP(amount)
        self.target.gain_MP(amount)

        self.entity.notify(
            f"# Mana Siphon\nTransferred **{amount} MP** to {self.target}."
        )
