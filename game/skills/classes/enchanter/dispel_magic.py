from typing import List, TYPE_CHECKING

from game.utils import distance
from game.skills.types.inplace_skill import InplaceSkill

if TYPE_CHECKING:
    from game.entities.entity import Entity


class DispelMagic(InplaceSkill):
    """
    Remove all harmful effects from allies within 7 meters radius.
    """

    def __init__(self, entity):
        super().__init__("Dispel Magic", 100, entity)

        self.active_time = 1
        self.casting_time = 4
        self.heal_factor = 0

        self.range = 16
        self.impact_range = 7

        self.mana_required = 2000

    def effect(self):
        if not self.entity.cell:
            return

        targets: List["Entity"] = list(
            filter(
                lambda e: distance(self.entity, e) <= self.impact_range * 16,
                self.entity.cell.get_allied_entities(self.entity),
            )
        )

        message = f"# {self.name}\n"
        message += (
            f"## Used {self.name} to remove harmful effects from nearby allies.\n"
        )
        message += "## Affected Targets\n"

        for target in targets:
            target.status_effects = list(
                filter(lambda s: not s.IS_HARMFUL, target.status_effects)
            )

            message += f" - {target}"

        if targets:
            self.entity.notify(message)

        else:
            self.entity.notify(f"# {self.name}\nNo targets found.")
