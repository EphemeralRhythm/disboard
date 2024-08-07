import random
from game.states.state import State
from game.states.entityStates.idleState import IdleState
from game.states.stateManager import StateManager


class Entity:
    def __init__(self, name, world):
        self.name = name

        self.id = 0
        self.x = 0
        self.y = 0
        self.grid_r = 0
        self.grid_c = 0
        self.hp = 0
        self.dir_x = 0
        self.dir_y = 0

        self.max_hp = 0
        self.level = 0

        self.directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        self.world = world
        self.cell = self.world.maps[self.grid_r][self.grid_c]

        self.idleState = IdleState(self)
        self.stateManager = StateManager(self, self.idleState)

        self.hp = 100
        self.attackRange = 16
        self.attackDamage = 10

    def __repr__(self):
        return f"{self.name}, {self.id}: {self.x}, {self.y} "

    def init_from_db_post(self, post: dict):
        self.x = post["x"]
        self.y = post["y"]
        self.grid_r = post["grid_r"]
        self.grid_c = post["grid_c"]
        self.hp = post["hp"]

    def init_from_spawn(self, x, y, grid_r, grid_c):
        self.x = x
        self.y = y
        self.grid_r = grid_r
        self.grid_c = grid_c

        self.dir_x, self.dir_y = random.choice(self.directions)
        self.hp = self.max_hp

    def update(self):
        self.stateManager.update()

    def changeState(self, state: State):
        self.stateManager.changeState(state)

    def take_damage(self, enemy):
        pass
