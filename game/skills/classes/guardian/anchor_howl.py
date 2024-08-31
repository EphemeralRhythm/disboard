from game.skills.types.inplace_skill import InplaceSkill
from game.utils import distance
from game.states.crowd_control_states.forced_state import ForcedState
from game.states.entityStates.attackState import AttackState


class AnchorHowl(InplaceSkill):
    def __init__(self, entity):
        super().__init__("Anchor Howl", 10, entity)

        self.active_time = 1
        self.casting_time = 1
        self.impact_range = 5

    def effect(self):
        enemies = self.entity.cell.get_targetable_entities(self.entity)
        targets = "Affected Targets:\n"

        for enemy in enemies:
            if distance(self.entity, enemy) <= self.impact_range * 16:
                targets += f"- {enemy}\n"

                enemy.notify(
                    f"{self.entity} used Anchor Howl forcing you to target them."
                )

                attack_state = AttackState(enemy, self.entity)
                forced_state = ForcedState(enemy, attack_state, 5)
                enemy.stateManager.changeState(forced_state)

        self.entity.notify("Using the skill **Anchor Howl**.\n" + targets)
