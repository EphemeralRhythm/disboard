from game.skills.types.entity_target_skill import EntityTargetSkill


class PhantomBlink(EntityTargetSkill):
    def __init__(self, entity):
        super().__init__("Phantom Blink", 10, entity)

        self.active_time = 1
        self.casting_time = 1

        self.use_range = 18
        self.range = 15 * 16

        self.REMOVES_STEALTH = False

    def effect(self):
        target = self.target
        assert target, "attempted Phantom Blink without a target"

        grid = target.cell.terrain

        rows = len(grid)
        cols = len(grid[0])

        nx = target.x - target.dir_x * 16
        ny = target.y + target.dir_y * 16

        nr = ny // 16
        nc = nx // 16

        if nr < 0 or nr >= rows or nc < 0 or nc >= cols or grid[nr][nr] == -2:
            nx = target.x
            ny = target.y

        self.entity.x = nx
        self.entity.y = ny

        self.entity.dir_x = -target.dir_x
        self.entity.dir_y = -target.dir_y

        self.entity.notify(f"Used the skill Phantom Blink to teleport behind {target}.")
