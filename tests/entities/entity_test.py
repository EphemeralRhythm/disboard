from game.entities.entity import Entity
from game.states.entityStates.moveState import MoveState
from game.states.entityStates.idleState import IdleState

async def main():
    player = Entity("Player1", None)

    player.update()  # Should be idling

    player.changeState(MovingState(player))
    player.update()  # Should be moving

    player.changeState(IdleState(player))
    player.update()  # Should be idling again
