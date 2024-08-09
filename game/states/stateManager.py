class StateManager:
    def __init__(self, entity, currentState):
        self.entity = entity
        self.currentState = currentState

    def changeState(self, newState, canceled=False):
        if self.currentState == newState:
            return

        if self.currentState is not None:
            self.currentState.OnExit(canceled)

        self.currentState = newState
        self.currentState.OnEnter()

    def update(self):
        if self.currentState is not None:
            self.currentState.OnUpdate()
