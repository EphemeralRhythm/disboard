from game.states.crowd_control_states.crowd_control_state import Crowd_Control_State

from game.states.state import State
from utils.constants import COLOR_YELLOW


class CastleInStoneState(State):
    def __init__(self, entity, timeout):
        super().__init__(entity)

        self.name = "castle in stone"
        self.action_name = "castle in stone"
        self.is_movement_locked = True
        self.time_remaining = timeout

    def OnUpdate(self):
        self.time_remaining -= 1

        if self.time_remaining == 0:
            self.Exit()

    def OnExit(self, canceled=False):
        self.entity.notify("### You are no longer immobile.", COLOR_YELLOW)
