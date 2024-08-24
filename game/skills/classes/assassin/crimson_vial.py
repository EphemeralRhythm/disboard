from game.skills.types.inplace_skill import InplaceSkill


class CrimsonVial(InplaceSkill):
    def __init__(self, entity):
        super().__init__("Crimson Vial", 10, entity)

        self.active_time = 1
        self.casting_time = 1

    def effect(self):
        amount = 0.2 * self.entity.MAX_HP
        self.entity.heal(amount)
        self.entity.notify(
            f"Used **Crimson Vial** to heal {amount} HP.\nYour HP is now {self.entity.HP}."
        )
