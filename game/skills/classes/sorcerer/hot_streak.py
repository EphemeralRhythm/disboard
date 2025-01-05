from game.skills.types.passive_skill import PassiveSkill


class HotStreak(PassiveSkill):
    def __init__(self, entity) -> None:
        super().__init__("Hot Streak", 0, entity)
