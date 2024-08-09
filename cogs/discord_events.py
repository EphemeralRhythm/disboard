import discord
import utils.constants
from discord.ext import tasks, commands


class DiscordEventHandler(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.send_event_feedback.start()

    @tasks.loop(seconds=10)
    async def send_event_feedback(self):
        events = self.client.world.get_events()

        for e in events:
            if not e.channel_id:
                continue

            channel = await self.client.fetch_channel(e.channel_id)
            embed = discord.Embed(description=e.description, color=e.color)

            await channel.send(content=f"<@{e.author_id}>", embed=embed)


def setup(client):
    client.add_cog(DiscordEventHandler(client))
