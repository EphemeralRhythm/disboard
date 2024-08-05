from multiprocessing.managers import BaseManager
from game.world import World

class ProcessManager(BaseManager):
    pass

ProcessManager.register('World', World)
