import discord
from discord.ext import commands
from models.interface.character_creation_view import CharacterCreationView
from utils.game import UNIT_COLORS, CLASSES


class Character(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def aschente(self, ctx):
        if self.client.world.has_player(str(ctx.author.id)):
            await ctx.send("You already are a member of the game system.")
            return

        await ctx.send(view=CharacterCreationView(ctx.author.id, self.client))


def setup(client):
    client.add_cog(Character(client))
