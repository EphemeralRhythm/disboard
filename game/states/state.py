class State:
    def __init__(self, entity):
        self.entity = entity
        self.name = "state"
        self.action_name = ""

        self.is_movement_locked = False

    def OnEnter(self):
        pass

    def OnExit(self, canceled=False):
        pass

    def OnUpdate(self):
        pass

    def Exit(self):
        self.entity.stateManager.changeState(self.entity.idleState)

    def OnTakeDamage(self):
        pass
