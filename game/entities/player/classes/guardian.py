from game.entities.player.player import Player


class Guardian(Player):
    def __init__(self, world, db_post):
        super().__init__(world, db_post)
