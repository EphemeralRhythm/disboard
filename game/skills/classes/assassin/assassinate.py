from game.skills.types.entity_target_skill import EntityTargetSkill


class Assassinate(EntityTargetSkill):
    """
    A finishing move that drains all your mana to do damage against an enemy.

    2000 mana ->  (2 * attack damage)
    4000 mana ->  (3 * attack damage)
    6000 mana ->  (4 * attack damage)
    8000 mana ->  (5 * attack damage)
    10000 mana -> (6 * attack damage)
    12000 mana -> (7 * attack damage)
    """

    def __init__(self, entity):
        super().__init__("Assassinate", 20, entity)

        self.active_time = 1
        self.casting_time = 1
        self.damage_factor = 4.2
        self.range = 16
        self.mana_required = 2000
        self.IS_INTERRUPT = True

    def effect(self):
        mana = self.entity.MP
        self.damage_factor = 2 + mana / 2000

        self.single_target_attack()
