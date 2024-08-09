async def check_player(client, ctx):
    player = client.world.get_player(str(ctx.author.id))
    if not player:
        await ctx.send("You are not a part of the game system.")

    return player


async def check_player_alive(client, ctx):
    player = client.world.get_player(str(ctx.author.id))
    if not player:
        await ctx.send("You are not a part of the game system.")
        return None

    if player.dead:
        await ctx.send("You are dead.")
        return None

    return player
