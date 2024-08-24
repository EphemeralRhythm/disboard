import discord
import asyncio

from utils.constants import COLOR_BLUE


async def get_location(client, ctx, player, prompt, max_range=0):
    await ctx.send(prompt)

    def check(m: discord.Message):
        return m.author.id == ctx.author.id

    msg = None
    try:
        msg = await client.wait_for("message", timeout=20, check=check)

    except asyncio.TimeoutError:
        return None

    print(msg.content)

    content = msg.content.split()
    if not len(content) == 2:
        await ctx.send("Invalid location.")
        return None

    try:
        x, y = map(int, content)

    except ValueError:
        await ctx.send("Invalid location.")
        return None

    if abs(x) + abs(y) > max_range:
        await ctx.send("Location entered is too far.")
        return None

    return (x, y)


async def get_accessible_location(
    client, ctx, player, prompt="Enter the location", max_range=0
):
    loc = await get_location(client, ctx, player, prompt, max_range)

    if not loc:
        return None

    x, y = loc

    nx = player.x + x * 16
    ny = player.y - y * 16

    nr = ny // 16
    nc = nx // 16

    grid = player.cell.terrain

    rows = len(grid)
    cols = len(grid[0])

    if nr < 0 or nr >= rows or nc < 0 or nc >= cols:
        await ctx.send("Location input is out of bounds.")
        return None

    if grid[nr][nc] == -2:
        await ctx.send("Location is inaccessible.")
        return None

    return (nx, ny)


async def send_target_select(client, targets, player, ctx, title):

    embed = discord.Embed(title=title, color=COLOR_BLUE)
    if targets:
        embed.description = "Select your target\n\n"
    else:
        embed.description = "No targets found."

    for i, t in enumerate(targets, 1):
        dist = (int((t.x - player.x) / 16), int((player.y - t.y) / 16))
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
        msg = await client.wait_for("message", timeout=20, check=check)

    except asyncio.TimeoutError:
        return None

    index = int(msg.content)
    return targets[index - 1]


async def get_skills_embed(player, ctx, client):
    embed = discord.Embed(title="Player Skills", color=COLOR_BLUE)

    if not player.skills:
        embed.description = "You don't have any skills yet!"
    else:
        embed.description = ""

    for i, skill in enumerate(player.skills, 1):
        embed.description += f"{i}. {skill.__repr__()}\n"

    await ctx.send(embed=embed)

    def check(m: discord.Message):
        return (
            m.author.id == ctx.author.id
            and m.channel == ctx.channel
            and m.content.isdigit()
            and 0 < int(m.content) <= len(player.skills)
            and player.skills[int(m.content) - 1].is_ready()
            and not player.stateManager.currentState.is_movement_locked
        )

    msg = None
    try:
        msg = await client.wait_for("message", timeout=20, check=check)

    except asyncio.TimeoutError:
        return None

    index = int(msg.content)
    return player.skills[index - 1]
