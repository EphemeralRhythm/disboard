import discord
from discord.ext import commands
from discord.ext.commands.core import guild_only
from models.interface.character_creation_view import CharacterCreationView
from utils.game import UNIT_COLORS, CLASSES


async def get_classes(ctx: discord.AutocompleteContext):
    if ctx.interaction.user.id == 660929334969761792:
        return ["warrior", "paladin", "theif"]
    else:
        return ["mage", "summoner"]


class Character(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def aschente(self, ctx):
        if self.client.world.has_player(str(ctx.author.id)):
            await ctx.send("You already are a member of the game system.")
            return

        await ctx.send(view=CharacterCreationView(ctx.author.id, self.client))

    @commands.slash_command(name="switch", guild_ids=[860943056248242176])
    async def switch_class(
        self,
        ctx: discord.ApplicationContext,
        classes: discord.Option(
            str, autocomplete=discord.utils.basic_autocomplete(get_classes)
        ),
    ):
        await ctx.response.send_message(f"You selected class {classes}")


def setup(client):
    client.add_cog(Character(client))
