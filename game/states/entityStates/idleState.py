from game.states.state import State


class IdleState(State):
    def __init__(self, entity):
        super().__init__(entity)

        self.name = "idle"
        self.action_name = "idling"

    def OnUpdate(self):
        print(f"{self.entity} is idling.")
