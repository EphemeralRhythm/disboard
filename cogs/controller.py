import asyncio
from functools import wraps

import discord
from discord.ext import commands
from game.command import Command
from modules.combat import send_target_select, get_skills_embed
from utils.constants import COLOR_RED
from modules.game import check_player, check_player_alive


class Controller(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="move")
    async def move(self, ctx, *args):
        if not (player := await check_player_alive(self.client, ctx)):
            return

        if player.is_movement_locked():
            await ctx.send("Unable to do that.")

        if len(args) != 2:
            await ctx.send("Invalid syntax.")
            return

        x, y = map(int, args)

        command = Command(
            name="move", author=player, x=player.x + x * 16, y=player.y - y * 16
        )
        self.client.world.add_command(command)

        await ctx.send("Command updated!")

    @commands.command(name="attack")
    async def attack(self, ctx):
        if not (player := await check_player_alive(self.client, ctx)):
            return

        if player.is_movement_locked():
            await ctx.send("Unable to do that.")

        targets = self.client.world.get_targetable_entities(player)
        target = await send_target_select(
            self.client, targets, player, ctx, "Attack command"
        )

        if target:
            command = Command(name="attack", author=player, target=target)
            self.client.world.add_command(command)
            await ctx.send(f"Command added to queue! Attacking {target}.")

    @commands.command(name="skills")
    async def skills(self, ctx):
        if not (player := await check_player_alive(self.client, ctx)):
            return

        skill = await get_skills_embed(player, ctx, self.client)

        if skill:
            command = await skill.initialize(player, ctx, self.client)

            if command:
                self.client.world.add_command(command)
                await ctx.send(f"Command added to queue, casting {skill.name}")


def setup(client):
    client.add_cog(Controller(client))
