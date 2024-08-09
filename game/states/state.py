class State:
    def __init__(self, entity):
        self.entity = entity
        self.name = "state"

        self.is_movement_locked = False

        self.did_enter = False

    def OnEnter(self):
        self.did_enter = True

    def OnExit(self, canceled=False):
        pass

    def OnUpdate(self):
        if not self.did_enter:
            self.OnEnter()
            self.OnUpdate()

    def Exit(self):
        self.entity.stateManager.changeState(self.entity.idleState)
