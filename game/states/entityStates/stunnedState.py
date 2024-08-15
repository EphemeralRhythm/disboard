from game.states.state import State

from utils.constants import COLOR_YELLOW


class StunnedState(State):
    def __init__(self, entity, timeout):
        super().__init__(entity)

        self.name = "stunned"
        self.action_name = "stunned"
        self.is_movement_locked = True
        self.time_remaining = timeout

    def OnUpdate(self):
        print(f"{self.entity} is stunned. {self.time_remaining} remaining.")
        if self.time_remaining == 0:
            self.Exit()

        self.time_remaining -= 1

    def OnExit(self, canceled=False):
        self.entity.notify("You are no longer stunned.", COLOR_YELLOW)
