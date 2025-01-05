from game.skills.types.entity_target_skill import EntityTargetSkill
from game.states.entityStates.followState import follow
from game.states.skill_states.guardian.shield_charge import ShieldChargeState


class ShieldCharge(EntityTargetSkill):
    """
    Charge towards an enemy with your shield dealing 400% attack damage to the primary target and dealing 130% attack damage to all enemies within 4 meters.

    Having the skill 'Shield Wall' active will boost attack damage on primary target up to 500% attack damage.
    """

    def __init__(self, entity):
        super().__init__("Shield Charge", 18, entity)

        self.active_time = 20
        self.casting_time = 1
        self.damage_factor = 4
        self.impact_range = 4
        self.range = 16

        self.mana_required = 5000

    def effect(self):
        if self.active_timeout == self.active_time:
            if not self.target:
                return

            state = ShieldChargeState(self.entity, self.target, 20, self)
            self.entity.changeState(state)
