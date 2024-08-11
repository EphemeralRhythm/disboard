from game.states.state import State
from game.utils import distance
from game.skills.skill import Skill
from game.states.entityStates.followState import follow


class CastState(State):
    def __init__(self, entity, skill: Skill):
        super().__init__(entity)

        self.name = "cast"
        self.skill = skill
        self.is_movement_locked = True

        self.casting = False

    def OnEnter(self):
        self.skill.use()

    def OnUpdate(self):
        target = self.skill.target
        entity = self.entity

        if not target or target.cell != entity.cell:
            self.Exit()
            return

        if not self.casting:
            if distance(target, entity) > self.skill.range:
                if not follow(entity, target):
                    self.Exit()
                return

            self.casting = True
            self.skill.use()

        print(f"{self.entity} is casting {self.skill}.")

        if self.skill.cast():
            self.Exit()

        self.entity.is_attacking = True
