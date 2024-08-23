from game.command import Command


class Skill:
    def __init__(self, name, cooldown, entity, x: int = 0, y: int = 0, target=None):
        self.name = name
        self.cooldown = cooldown
        self.cooldown_timeout = 0
        self.entity = entity

        self.use_range = 15 * 16
        self.range = 16

        self.casting_time = 1
        self.casting_timeout = 0

        self.active_time = 1
        self.active_timeout = 0

        self.casting = False
        self.active = False

        self.x = x
        self.y = y
        self.target = target

        self.IS_PASSIVE = False
        self.GENERATES_THREAT = True
        self.REMOVES_STEALTH = True
        self.ALLOW_WHILE_STUNNED = False
        self.REQUIRES_TARGET = False

    def cast(self):
        assert self.casting, "Attempted to update before casting started"

        self.casting_timeout -= 1

        if self.casting_timeout == 0:
            self.activate()
            return True

        return False

    def update(self):
        if self.casting:
            return

        elif self.active:
            self.effect()
            self.active_timeout -= 1

            if self.active_timeout == 0:
                self.active = False
                self.cooldown_timeout = self.cooldown

        elif self.cooldown_timeout > 0:
            self.cooldown_timeout -= 1

    def is_ready(self):
        return not self.active and not self.casting and self.cooldown_timeout == 0

    def use(self):
        assert self.is_ready(), "attempted to use when skill was not ready"

        self.casting = True
        self.casting_timeout = self.casting_time
        print(f"{self.entity} is casting {self.name}.")
        self.entity.notify(f"Casting {self.name} now.")

    def activate(self):
        self.casting = False
        self.active = True
        self.active_timeout = self.active_time

    def effect(self):
        raise NotImplementedError()

    def __repr__(self):
        name = self.name
        if self.casting:
            name += f" - (Casting, activates in {self.casting_timeout})"
        elif self.active:
            name += f" - (Active, fades in {self.active_timeout})"
        elif self.cooldown_timeout == 0:
            name += " - (Ready)"
        else:
            name += f" - (Available in {self.cooldown_timeout})"

        return name

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, Skill):
            return self.name == __value.name

        return False

    async def initialize(self, player, ctx, client) -> Command | None:
        raise NotImplementedError()
