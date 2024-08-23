import discord

from utils.constants import COLOR_CYAN
from utils.game import classes_emoji

from discord.ext import commands
from discord.ext.commands import has_permissions
from discord import File


class Admin(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="ping")
    async def ping(self, ctx):
        self.client.logger.info("testing the logs!")
        await ctx.send("pong")

    @commands.command()
    @has_permissions(administrator=True)
    async def say(self, ctx, args):
        content = " ".join(ctx.message.content.split()[1:])
        print("content: ", content)
        await ctx.message.delete()
        await ctx.send(content)

    @commands.command()
    @has_permissions(administrator=True)
    async def purge(self, ctx, limit: int):
        limit = min(limit, 100)
        await ctx.channel.purge(limit=limit)
        await ctx.send("Cleared by {}".format(ctx.author.mention))

    @commands.command()
    @has_permissions(administrator=True)
    async def logs(self, ctx):
        await ctx.send(file=File("./logs/infos.log"))

    @commands.command()
    @has_permissions(administrator=True)
    async def classes_embed(self, ctx):
        embed = discord.Embed()
        embed.color = COLOR_CYAN
        d = ""
        for cl in classes_emoji:
            d += f"- {classes_emoji[cl]} {cl.title()}\n"
        embed.description = d

        embed.title = "Avaialble Classes"
        message = await ctx.send(embed=embed)

        for cl in classes_emoji:
            await message.add_reaction(classes_emoji[cl])


def setup(client):
    client.add_cog(Admin(client))
