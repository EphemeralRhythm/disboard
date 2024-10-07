from typing import TYPE_CHECKING, Optional, List

if TYPE_CHECKING:
    from game.status_effects.status_effect import StatusEffect
    from game.states.crowd_control_states.crowd_control_state import Crowd_Control_State
    from game.skills.skill import Skill


class Support:
    def __init__(
        self,
        heal,
        mana,
        source: "Optional[Skill]",
    ):

        self.heal = heal
        self.status_effects: "List[StatusEffect]" = []
        self.mana = mana
        self.source = source
