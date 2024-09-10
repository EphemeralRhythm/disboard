from game.entities.player.player import Player
from game.combat.attack import Attack


class Assassin(Player):
    def __init__(self, world, db_post):
        super().__init__(world, db_post)

        self.MAX_MP = 12000

        self.HP = 11360
        self.ATK = 570
        self.ATK = 330

        self.DEF = 200
        self.CRIT = 40

    def on_leave_combat(self):
        self.MP = 0

    def on_attack(self, attack: "Attack"):
        if attack.source and attack.source.mana_gained != 0 and attack.did_crit:
            self.gain_MP(2000)
