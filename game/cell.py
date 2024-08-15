import json
from game.entities.player import Player
from game.entities.entity import Entity
from game.utils import distance


class Cell:
    def __init__(self, world, id=0, grid_r=0, grid_c=0):

        self.id = id

        self.grid_r = grid_r
        self.grid_c = grid_c

        self.players = set()
        self.entities = {}
        self.map_objects = []

        self.world = world

        self.base_image_path = f"./assets/images/maps/{self.id}.png"

        self.spawn_regions = []

        with open(f"./assets/data/maps/{self.id}.json") as f:
            self.data = json.load(f)

        self.rows = self.data["rows"]
        self.cols = self.data["cols"]

        self.size = (16 * self.cols, 16 * self.rows)

        # 2d grid for terrain (representing heights)
        self.terrain = self.data["terrain"]

    def add_player(self, player):
        self.players.add(player)

    def remove_player(self, player):
        if player not in self.players:
            return False

        self.players.remove(player)
        return True

    def spawn_entity(self, entity):
        self.entities[entity.id] = entity

    def __repr__(self) -> str:
        return f"[Cell] : [id: {self.id}, r: {self.grid_r}, c: {self.grid_c}]"

    def update(self):

        for entity in self.entities:
            print(entity)
            self.entities[entity].update()

    def get_all_entities(self):
        return list(self.entities.values()) + list(self.players)

    def get_targetable_entities(self, player: Player, x=0, y=0):
        x = player.x + x * 16
        y = player.y - y * 16

        def is_attackable(e: Entity):
            if abs(x - e.x) + abs(y - e.y) > 16 * 5:
                return False

            if isinstance(e, Player):
                return e.id != player.id and not player.is_ally(e)

            return e.hostility_level != Entity.HOSTILITY_LEVEL_FRIENDLY

        entities = list(filter(is_attackable, self.get_all_entities()))
        entities.sort(key=lambda x: distance(player, x))

        return entities
