from game.states.state import State
from game.utils import distance
from game.skills.skill import Skill
from game.states.entityStates.followState import follow


class CastState(State):
    def __init__(self, entity, skill: Skill, previous_state: State):
        super().__init__(entity)

        self.name = "cast"
        self.action_name = "casting"
        self.skill = skill
        self.is_movement_locked = True

        self.casting = False
        self.previous_state = previous_state

    def OnUpdate(self):
        target = self.skill.target
        entity = self.entity
        print(f"{self.entity} is using a skill")

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
            return

        if self.skill.cast():
            self.Exit()

        self.entity.is_attacking = True

    def Exit(self):
        if self.previous_state:
            self.entity.stateManager.changeState(self.previous_state)
        else:
            super().Exit()
