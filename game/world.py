import utils.database as db

from game.cell import Cell
from game.entities.player import Player


class World:
    def __init__(self):
        self.grid = [[1]]

        self.rows = len(self.grid)
        self.cols = len(self.grid[0])

        self.maps = [[Cell(1, 0, 0) for c in range(self.cols)] for r in range(self.rows)]
        self.init_maps()

        self.players = {}

    def init_maps(self):
        for r in range(self.rows):
            for c in range(self.cols):
                self.maps[r][c] = Cell(self.grid[r][c], r, c)

    def update(self):
        for r in range(self.rows):
            for c in range(self.cols):
                self.maps[r][c].update()

    def add_player(self, post):
        player = Player(self, post)
        
        r = player.grid_r
        c = player.grid_c
        self.players[post["_id"]]  = player

        self.maps[r][c].add_player(player)

    def init_players(self):
        for player in db.players_collection.find():
            self.add_player(player)

    def has_player(self, id):
        return db.players_collection.find_one({"_id": id}) is not None

    def create_player(self, id: str, gender, cl, color) -> bool:
        if self.has_player(id):
            return False

        post = {}
        post['_id'] = id

        # x and y are placeholders
        # change after adding spawn location(s)
        post['x'] = 50
        post['y'] = 50
        post['grid_r'] = 0
        post['grid_c'] = 0

        # also placeholders
        post['hp'] = 100
        post['gender'] = gender
        post['class'] = cl
        post['color'] = color

        self.add_player(post)
        db.players_collection.insert_one(post)
        return True


    def get_players(self) -> dict:
        return self.players
