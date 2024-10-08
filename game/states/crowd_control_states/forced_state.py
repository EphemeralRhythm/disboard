from game.states.crowd_control_states.crowd_control_state import Crowd_Control_State
from game.states.state import State

from utils.constants import COLOR_YELLOW


class ForcedState(Crowd_Control_State):
    def __init__(self, entity, state: State, timeout):
        super().__init__(entity)

        self.state = state
        self.name = "forced " + state.name
        self.action_name = "crowd controlled"

        self.is_movement_locked = True
        self.time_remaining = timeout

    def OnUpdate(self):
        self.state.OnUpdate()
        self.time_remaining -= 1

        if self.time_remaining == 0:
            self.Exit()

    def OnExit(self, canceled=False):
        self.entity.notify("### You are no crowd controlled.", COLOR_YELLOW)
