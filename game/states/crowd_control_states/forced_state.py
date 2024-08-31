from game.states.state import State

from utils.constants import COLOR_YELLOW


class ForcedState(State):
    def __init__(self, entity, state: State, timeout):
        super().__init__(entity)

        self.state = state
        self.name = "forced " + state.name
        self.action_name = "crowd controlled"

        self.is_movement_locked = True
        self.time_remaining = timeout

        self.IS_STATUS_EFFECT = True

    def OnUpdate(self):
        self.state.OnUpdate()
        self.time_remaining -= 1

        if self.time_remaining == 0:
            self.Exit()

    def OnExit(self, canceled=False):
        self.entity.notify("You are no crowd controlled.", COLOR_YELLOW)
