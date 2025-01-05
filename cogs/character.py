import discord
from discord.ext import commands
from discord.ext.commands.core import guild_only
from models.interface.character_creation_view import CharacterCreationView
from utils.game import UNIT_COLORS, CLASSES
from game.command import Command


class Character(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def aschente(self, ctx):
        if self.client.world.has_player(str(ctx.author.id)):
            await ctx.send("You already are a member of the game system.")
            return

        await ctx.send(view=CharacterCreationView(ctx.author.id, self.client))

    @commands.command()
    async def set_channel(self, ctx):
        player = self.client.world.get_player(str(ctx.author.id))

        if not player:
            await ctx.send("You are not a part of the game system.")
            return

        command = Command(name="set_channel", author=player, x=ctx.channel.id)

        self.client.world.add_command(command)

        await ctx.send("Command added to queue!")

    @commands.command()
    async def change_class(self, ctx, arg):
        player = self.client.world.get_player(str(ctx.author.id))

        if not player:
            await ctx.send("You are not a part of the game system.")
            return

        if arg not in CLASSES:
            await ctx.send("invalid class")
            return

        self.client.world.change_player_class(player, arg)
        await ctx.send("done")


def setup(client):
    client.add_cog(Character(client))
