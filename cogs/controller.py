import discord

import asyncio
from discord.ext import commands
from game.command import Command
from utils.constants import COLOR_RED


class Controller(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="move")
    async def move(self, ctx, *, args):
        print("args: ", args)
        player = self.client.world.get_player(str(ctx.author.id))
        if not player:
            await ctx.send("You are not a part of the game system.")
            return

        args = args.split()

        if len(args) != 2:
            await ctx.send("Invalid syntax.")
            return

        x, y = map(int, args)

        command = Command(
            name="move", author=player, x=player.x + x * 16, y=player.y + y * 16
        )
        self.client.world.add_command(command)

        await ctx.send("Command updated!")

    @commands.command(name="attack")
    async def attack(self, ctx):
        player = self.client.world.get_player(str(ctx.author.id))
        if not player:
            await ctx.send("You are not a part of the game system.")
            return

        targets = self.client.world.get_targetable_entities(player)

        embed = discord.Embed(title="Attack Command", color=COLOR_RED)
        embed.description = "Select the entity that you want to attack\n\n"

        for i, t in enumerate(targets, 1):
            dist = ((t.x - player.x) // 16, (player.y - t.y) // 16)
            embed.description += f"{i}. {t.__repr__().title()} {dist}\n"

        await ctx.send(embed=embed)

        def check(m: discord.Message):
            return (
                m.author.id == ctx.author.id
                and m.channel == ctx.channel
                and m.content.isdigit()
                and 0 < int(m.content) <= len(targets)
            )

        msg = None
        try:
            msg = await self.client.wait_for("message", timeout=20, check=check)

        except asyncio.TimeoutError:
            pass

        assert msg
        index = int(msg.content)
        command = Command(name="attack", author=player, target=targets[index - 1])
        self.client.world.add_command(command)

        await ctx.send(f"Command added to queue! Attacking {targets[index - 1]}.")


def setup(client):
    client.add_cog(Controller(client))
