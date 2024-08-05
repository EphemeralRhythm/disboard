from discord.ext import commands
from discord.ext.commands import has_permissions
from discord import File

class Admin(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="ping")
    async def ping(self, ctx):
        self.client.logger.info("testing the logs!")
        await ctx.send("pong")

    @commands.command()
    @has_permissions(administrator=True)
    async def purge(self, ctx, limit: int):
        limit = min(limit, 100)
        await ctx.channel.purge(limit=limit)
        await ctx.send('Cleared by {}'.format(ctx.author.mention))

    @purge.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("Missing Permissions!")

    @commands.command()
    @has_permissions(administrator=True)
    async def logs(self, ctx):
        await ctx.send(file=File("./logs/infos.log"))


async def setup(client):
    await client.add_cog(Admin(client))
