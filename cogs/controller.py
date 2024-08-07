from discord.ext import commands


class Controller(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="move")
    async def move(self, ctx, *, args):
        print("args: ", args)
        player = self.client.world.get_player(str(ctx.author.id))
        print("Players fetched: ", player)

        if not player:
            await ctx.send("You are not a part of the game system.")
            return

        args = args.split()

        if len(args) != 2:
            await ctx.send("Invalid syntax.")
            return

        x, y = map(int, args)

        player.move(player.x + x * 16, player.y - y * 16)
        self.client.world.set_player(player)

        await ctx.send("Command updated!")


def setup(client):
    client.add_cog(Controller(client))
