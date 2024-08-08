from game.states.state import State
from game.skills.skill import Skill


class castState(State):
    def __init__(self, entity, skill: Skill):
        super().__init__(entity)

        self.name = "cast"
        self.skill = skill

    def OnUpdate(self):
        print(f"{self.entity} is casting {self.skill}.")

        if self.skill.cast():
            self.Exit()
