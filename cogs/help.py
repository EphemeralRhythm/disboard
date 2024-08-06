import discord
import utils.constants
from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="help")
    async def help(self, ctx):
        color = utils.constants.COLOR_PINK
        embed = discord.Embed(title="Schwi Help", color=color)
        description = "Placeholder"

        description += ""
        embed.description = description
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Help(client))
