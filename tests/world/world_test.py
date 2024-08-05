import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from game.world import World

world = World()

print(world.maps[0][0])
print(world.maps[0][0].terrain)
