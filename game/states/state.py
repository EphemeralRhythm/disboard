class State:
    def __init__(self, entity):
        self.entity = entity
        self.name = "state"

        self.is_movement_locked = False

    def OnEnter(self):
        pass

    def OnExit(self):
        pass

    def OnUpdate(self):
        pass

    def Exit(self):
        self.entity.stateManager.changeState(self.entity.idleState)
