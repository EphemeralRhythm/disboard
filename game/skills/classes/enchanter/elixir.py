from game.skills.types.inplace_skill import InplaceSkill
from game.status_effects.buffs.heal_buff import HealBuffStatusEffect


class Elixir(InplaceSkill):
    """
    Enhances the healing potential of allies with recovery skills.
    """

    def __init__(self, entity):
        super().__init__("Elixir", 15, entity)

        self.active_time = 1
        self.casting_time = 1
        self.damage_factor = 0
        self.range = 16

        self.mana_gained = 1000

    def effect(self):
        self.status_effects = [HealBuffStatusEffect(self.target, 6, 200)]
        targets = self.multi_target_support()

        if targets:
            message = f"# {self.name}"
            message += "## Used the skill elixir to boost the healing potential of nearby allies.\n"
            message += "## Affected Targets\n"

            for target in targets:
                message += f"- {target.name}\n"

            self.entity.notify(message)
