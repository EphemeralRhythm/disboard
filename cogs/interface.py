import discord
from discord.ext import commands
from modules.map_ui import draw_map

from modules.game import check_player_alive, check_player
from utils.constants import COLOR_CYAN

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from game.entities.player.player import Player


class Interface(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="map")
    async def _map(self, ctx, *, args=""):

        if not (unit := await check_player_alive(self.client, ctx)):
            return

        image = draw_map(
            unit.x, unit.y, unit.cell, ("o" in args), unit, "g" not in args
        )

        path = f"./assets/images/player_maps/{ctx.author.id}.png"
        image.save(path)

        await ctx.reply(file=discord.File(path))

    @commands.command(name="status")
    async def status(self, ctx):
        player = await check_player_alive(self.client, ctx)

        if not player:
            return

        embed = discord.Embed(title=f"{ctx.author.name}", color=COLOR_CYAN)

        embed.add_field(
            name="Health",
            value=f"{player.HP}/{player.MAX_HP} ({int(player.HP / player.MAX_HP * 100)} %)",
        )

        embed.add_field(
            name="Mana",
            value=f"{player.MP}/{player.MAX_MP} ({int(player.MP / player.MAX_MP * 100)} %)",
        )

        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Interface(client))
