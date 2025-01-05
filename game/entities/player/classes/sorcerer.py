from game.entities.player.player import Player
from game.combat.attack import Attack


class Sorcerer(Player):
    def __init__(self, world, db_post):
        super().__init__(world, db_post)

        self.MAX_MP = 16000
        self.MP = 16000

        self.crit_counter = 0

    def on_leave_combat(self):
        self.MP = self.MAX_MP

    def on_attack(self, attack: "Attack"):
        if self.has_skill("Hot Streak"):
            if attack.did_crit:
                self.crit_counter += 1
            else:
                self.crit_counter = 0

            if self.crit_counter == 2:
                self.crit_counter = 0
                self.remove_skill_cooldown("")
