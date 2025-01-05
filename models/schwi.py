import discord
import settings

from discord.ext import commands

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.world import World


class Schwi(commands.Bot):
    def __init__(self, world: "World") -> None:
        intents = discord.Intents.all()
        super().__init__(command_prefix=".", intents=intents, help_command=None)

        self.logger = settings.logging.getLogger("discord")
        self.world = world

        self.players = {}

    async def on_ready(self):
        assert self.user
        self.logger.info(f"User: {self.user} (ID: {self.user.id})")

        for cog_file in settings.COGS_DIR.glob("*.py"):
            if cog_file.name != "__init__.py":
                self.load_extension(f"cogs.{cog_file.name[:-3]}")

    async def load(self, ctx, cog: str):
        self.load_extension(f"cogs.{cog.lower()}")

    async def unload(self, ctx, cog: str):
        self.unload_extension(f"cogs.{cog.lower()}")

    async def reload(self, ctx, cog: str):
        self.reload_extension(f"cogs.{cog.lower()}")
