from game.skills.skill import Skill


class SpotTargetSkill(Skill):
    def __init__(self, name, cooldown, entity):
        super().__init__(name, cooldown, entity)
