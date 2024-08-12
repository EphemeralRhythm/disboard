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


async def check_player_locked(player, ctx):
    if player.is_movement_locked():
        await ctx.send(
            f"Unable to perform this action while {player.stateManager.currentState.action_name}"
        )
        return True
    return False


async def check_player_silenced(player, ctx):
    if player.is_silenced():
        await ctx.send("Unable to perform this action at the moment.")
        return True
    return False
