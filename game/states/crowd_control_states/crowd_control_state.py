from game.states.state import State


class Crowd_Control_State(State):
    def __init__(self, entity):
        super().__init__(entity)

        self.IS_CROWD_CONTROL = True
        self.time_remaining = 0

    def __repr__(self) -> str:
        return f"{self.name} - ({self.time_remaining})"
