import discord
from discord.ext import commands
from modules.map_ui import draw_map


class Interface(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="map")
    async def _map(self, ctx):
        players = self.client.world.get_players()

        if str(ctx.author.id) not in players:
            await ctx.send("You are not a part of the game system.")
            return

        unit = players[str(ctx.author.id)]
        image = draw_map(unit.x, unit.y, unit.cell)

        path = f"./assets/images/player_maps/{ctx.author.id}.png"
        print("Path: ", path)
        image.save(path)

        await ctx.reply(file=discord.File(path))


def setup(client):
    client.add_cog(Interface(client))
