from typing import TYPE_CHECKING, Optional, List

if TYPE_CHECKING:
    from game.status_effects.status_effect import StatusEffect
    from game.states.crowd_control_states.crowd_control_state import Crowd_Control_State
    from game.skills.skill import Skill


class Attack:
    def __init__(
        self, damage, acc, source: "Optional[Skill]", enemy_str="", attacker=None
    ):

        self.damage = damage
        self.acc = acc

        self.aggro_factor = 1

        self.crit_rate = 10
        self.crit_multiplier = 1.5

        self.is_dodgeable = True
        self.is_interrupt = False
        self.is_critable = True

        self.status_effects: "List[StatusEffect]" = []
        self.crowd_control_state: "Optional[Crowd_Control_State]" = None

        self.enemy_str = enemy_str
        self.attacker = attacker

        self.variance = 10

        self.source = source
        self.did_crit = False
