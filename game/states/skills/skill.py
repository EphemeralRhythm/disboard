class Skill:
    def __init__(self, name, cooldown, entity):
        self.name = name
        self.cooldown = cooldown
        self.cooldown_timeout = 0
        self.entity = entity

        self.casting_time = 1
        self.casting_timeout = 0

        self.active_time = 1
        self.active_timeout = 0

        self.casting = False
        self.active = False

    def update(self):
        if self.casting:
            self.casting_timeout -= 1

            if self.casting_timeout == 0:
                self.activate()

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
        assert self.is_ready()

        self.casting = True
        self.casting_timeout = self.casting_time

    def activate(self):
        self.casting = False
        self.active = True
        self.active_timeout = self.active_time

    def effect(self):
        raise NotImplementedError()
