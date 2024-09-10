import asyncio
from functools import wraps

import discord
from discord.ext import commands
from game.command import Command
from modules.combat import send_target_select, get_skills_embed
from utils.constants import COLOR_CYAN, COLOR_RED
from modules.game import (
    check_player,
    check_player_alive,
    check_player_silenced,
    check_player_locked,
)


class Controller(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="move", aliases=["m"])
    async def move(self, ctx, *args):
        """ """
        if not (player := await check_player_alive(self.client, ctx)):
            return

        if await check_player_locked(player, ctx):
            return

        if len(args) != 2:
            await ctx.send("Invalid syntax.")
            return

        x, y = map(int, args)

        command = Command(
            name="move", author=player, x=player.x + x * 16, y=player.y - y * 16
        )
        self.client.world.add_command(command)

        await ctx.send("Command updated!")

    @commands.command(name="attack", aliases=["a"])
    async def attack(self, ctx, *args):
        if not (player := await check_player_alive(self.client, ctx)):
            return

        if await check_player_locked(player, ctx):
            return

        if len(args) != 2:
            args = ("0", "0")

        def isdigit(a):
            for c in a:
                if c not in "0123456789-":
                    return False
            return True

        for a in args:
            if not isdigit(a):
                args = (0, 0)

        args = list(map(int, args))

        targets = self.client.world.get_targetable_entities(player, args[0], args[1])
        target = await send_target_select(
            self.client, targets, player, ctx, "Attack command"
        )

        if target:
            command = Command(name="attack", author=player, target=target)
            self.client.world.add_command(command)
            embed = discord.Embed(
                description=f"Command added to queue! Attacking {target.get_name()}.",
                color=COLOR_CYAN,
            )
            await ctx.send(embed=embed)

    @commands.command(name="skills", aliases=["s"])
    async def skills(self, ctx, arg=None):
        if not (player := await check_player_alive(self.client, ctx)):
            return

        if arg not in ["c", "n", "info"]:
            arg = None

        skill = await get_skills_embed(player, ctx, self.client, arg == "info")
        if skill:
            if arg == "info":
                embed = skill.get_info_embed()
                await ctx.send(embed=embed)
                return

            command = await skill.initialize(player, ctx, self.client, arg)

            if command:
                if await check_player_silenced(
                    player, ctx
                ) or await check_player_locked(player, ctx):
                    return

                self.client.world.add_command(command)
                await ctx.send(f"Command added to queue, using the skill {skill.name}")


def setup(client):
    client.add_cog(Controller(client))
