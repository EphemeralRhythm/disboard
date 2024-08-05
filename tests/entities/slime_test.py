import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from game.entities.mobs.slime.slime import Slime

slime = Slime(2, 2, 2, 2, None)

assert slime.hp == slime.MAX_HP
assert slime.x == 2

