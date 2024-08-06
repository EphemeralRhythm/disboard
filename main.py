import multiprocessing
from multiprocessing.managers import BaseManager
from game.world import World

import settings
from models.schwi import Schwi
from models.backend import Backend

logger = settings.logging.getLogger("bot")


def run_backend(world):
    backend = Backend(world)
    backend.update_game()


def run_bot(world):
    bot = Schwi(world)

    assert settings.DISCORD_API_SECRET
    bot.run(settings.DISCORD_API_SECRET)


class ProcessManager(BaseManager):
    pass


ProcessManager.register("World", World)

if __name__ == "__main__":

    with ProcessManager() as manager:
        world = manager.World()

        game_backend_process = multiprocessing.Process(
            target=run_backend, args=(world,)
        )
        discord_bot_process = multiprocessing.Process(target=run_bot, args=(world,))

        game_backend_process.start()
        discord_bot_process.start()

        game_backend_process.join()
        discord_bot_process.join()
