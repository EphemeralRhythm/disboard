from game.skills.generic.taunt import Taunt


class TauntingShout(Taunt):
    def __init__(self, entity):
        super().__init__(entity, "Taunting Shout", 20)
