import discord
from discord.ext import commands
from modules.map_ui import draw_map

from modules.game import check_player_alive


class Interface(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="map")
    async def _map(self, ctx, *, args=None):

        if not (unit := await check_player_alive(self.client, ctx)):
            return

        image = draw_map(unit.x, unit.y, unit.cell, bool(args), unit)

        path = f"./assets/images/player_maps/{ctx.author.id}.png"
        image.save(path)

        await ctx.reply(file=discord.File(path))


def setup(client):
    client.add_cog(Interface(client))
