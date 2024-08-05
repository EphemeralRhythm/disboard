import json

class Cell:
    def __init__(self, id= 0, grid_r= 0, grid_c= 0):

        self.id = id

        self.grid_r = grid_r
        self.grid_c = grid_c

        self.players = set()
        self.entities = []
        self.map_objects = []

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
        assert(player in self.players)
        self.players.remove(player)

    def __repr__(self) -> str:
        return f"[Cell] : [id: {self.id}, r: {self.grid_r}, c: {self.grid_c}]"

    def update(self):
        print("players in cell: ", self.players)
        for entity in self.entities:
            entity.update()

        for player in self.players:
            player.update()
