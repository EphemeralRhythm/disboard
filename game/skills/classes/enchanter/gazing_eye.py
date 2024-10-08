from game.skills.types.entity_target_skill import EntityTargetSkill
from game.status_effects.debuffs.defense_debuff import DefenseDebuffStatusEffect


class GazingEye(EntityTargetSkill):
    """
    Inflicts a 40% defense debuff to the target.
    This skill can not be used if the enchanter has head gear equipped.
    """

    def __init__(self, entity):
        super().__init__("Gazing Eye", 10, entity)

        self.active_time = 1
        self.casting_time = 1
        self.damage_factor = 0
        self.effect_time = 10
        self.range = 16

        self.mana_gained = 1000

    async def initialize(self, player, ctx, client, arg=None):
        # add condition for head gear

        return await super().initialize(player, ctx, client, arg)

    def effect(self):
        self.status_effects = [
            DefenseDebuffStatusEffect(self.target, self.effect_time, 40)
        ]
        self.single_target_attack()
