from game.states.state import State
from game.skills.skill import Skill


class CastState(State):
    def __init__(self, entity, skill: Skill):
        super().__init__(entity)

        self.name = "cast"
        self.skill = skill
        self.is_movement_locked = True

    def OnEnter(self):
        super().OnEnter()
        print("HIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII")
        self.skill.use()

    def OnUpdate(self):
        super().OnUpdate()
        print("DID ENTER???? ", self.did_enter)
        print(f"{self.entity} is casting {self.skill}.")

        if self.skill.cast():
            self.Exit()

        self.entity.is_attacking = True
