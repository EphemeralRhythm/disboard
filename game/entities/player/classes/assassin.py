from game.entities.player.player import Player


class Assassin(Player):
    def __init__(self, world, db_post):
        super().__init__(world, db_post)

    def on_leave_combat(self):
        self.MP = 0
