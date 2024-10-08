from game.skills.types.inplace_skill import InplaceSkill
from game.utils import distance
from game.states.crowd_control_states.forced_state import ForcedState
from game.states.entityStates.attackState import AttackState

from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from game.entities.entity import Entity


class AnchorHowl(InplaceSkill):
    """
    Raise a loud cry forcing all the enemies within 4 meters to attack you for 5 ticks.
    """

    def __init__(self, entity):
        super().__init__("Anchor Howl", 30, entity)

        self.active_time = 1
        self.casting_time = 1
        self.impact_range = 4
        self.effect_time = 5

    def effect(self):
        if not self.entity.cell:
            self.entity.idle()
            return

        enemies: "List[Entity]" = self.entity.cell.get_targetable_entities(self.entity)
        targets = "Affected Targets:\n"

        for enemy in enemies:
            if distance(self.entity, enemy) <= self.impact_range * 16:
                targets += f"- {enemy}\n"

                enemy.notify(
                    f"{self.entity} used Anchor Howl forcing you to target them."
                )

                attack_state = AttackState(enemy, self.entity)
                forced_state = ForcedState(enemy, attack_state, self.effect_time)
                enemy.stateManager.changeState(forced_state)

        self.entity.notify("Using the skill **Anchor Howl**.\n" + targets)
