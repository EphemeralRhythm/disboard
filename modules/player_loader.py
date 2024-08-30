from game.skills.classes.assassin.atropy_break import AtrophyBreak
from game.skills.classes.assassin.ghost_step import GhostStep
from game.skills.classes.assassin.shadow_cloak import ShadowCloak
from game.skills.classes.assassin.phantom_blink import PhantomBlink
from game.skills.classes.assassin.crimson_vial import CrimsonVial
from game.skills.classes.assassin.blind import Blind
from game.skills.classes.assassin.smoke_screen import SmokeScreen
from game.skills.classes.assassin.death_sweep import DeathSweep
from game.skills.classes.assassin.backstab import Backstab
from game.skills.classes.assassin.assassinate import Assassinate


def update_skills(player):
    match player.player_class:
        case "assassin":
            player.skills.append(GhostStep(player))
            player.skills.append(ShadowCloak(player))
            player.skills.append(PhantomBlink(player))
            player.skills.append(CrimsonVial(player))
            player.skills.append(AtrophyBreak(player))
            player.skills.append(Blind(player))
            player.skills.append(SmokeScreen(player))
            player.skills.append(Assassinate(player))
            player.skills.append(Backstab(player))
            player.skills.append(DeathSweep(player))
