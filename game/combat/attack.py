class Attack:
    def __init__(self, damage, acc, enemy_str="", attacker=None):

        self.damage = damage
        self.acc = acc

        self.aggro_factor = 1

        self.crit_rate = 10
        self.crit_multiplier = 1.5

        self.is_dodgeable = True
        self.is_interrupt = False
        self.is_critable = True

        self.status_effects = []
        self.crowd_control_state = None

        self.enemy_str = enemy_str
        self.attacker = attacker

        self.variance = 10
