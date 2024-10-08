from game.skills.types.inplace_skill import InplaceSkill


class ImpendingVictory(InplaceSkill):
    """ """

    def __init__(self, entity):
        super().__init__("Impending Victory", 20, entity)

        self.active_time = 1
        self.casting_time = 1
        self.GENERATES_THREAT = False
        self.IS_CRITABLE = False

    def effect(self):
        amount = 0.2 * self.entity.MAX_HP
        self.entity.heal(amount)
        self.entity.notify(
            f"## Impending Victory\nUsed **Impending victory** to heal {amount} HP.\nYour HP is now {self.entity.HP}."
        )
