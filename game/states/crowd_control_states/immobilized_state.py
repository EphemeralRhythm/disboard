from game.states.crowd_control_states.crowd_control_state import Crowd_Control_State

from utils.constants import COLOR_YELLOW


class ImmobilizedState(Crowd_Control_State):
    def __init__(self, entity, timeout):
        super().__init__(entity)

        self.name = "immobilized"
        self.action_name = "immobilized"
        self.is_movement_locked = True
        self.time_remaining = timeout

    def OnUpdate(self):
        self.time_remaining -= 1

        if self.time_remaining == 0:
            self.Exit()

    def OnExit(self, canceled=False):
        self.entity.notify("### You are no longer immobile.", COLOR_YELLOW)
