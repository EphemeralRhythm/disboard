from game.skills.skill import Skill


class InplaceSkill(Skill):
    def __init__(self, name, cooldown, entity):
        super().__init__(name, cooldown, entity)
