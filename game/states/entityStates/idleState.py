from game.states.state import State


class IdleState(State):
    def __init__(self, entity):
        super().__init__(entity)

        self.name = "idle"

    def OnUpdate(self):
        print(f"{self.entity} is idling.")

    def OnExit(self, canceled=False):
        print("BYYYYYYYYYYYEEEEEE")
