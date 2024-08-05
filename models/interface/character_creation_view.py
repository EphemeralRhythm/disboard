import discord

from typing import Optional
from utils.game import CLASSES

colors = ["red", "blue", "green", "yellow", "orange"]
class_options = []
gender_options = []
color_options = []

class CharacterCreationView(discord.ui.View):
    def __init__(self, author_id, client):
        super().__init__(timeout=180)

        self.selected_gender = "male"
        self.selected_class = "warrior"
        self.selected_color = "blue"

        self.author_id = author_id
        self.client = client

        for cl in CLASSES:
            class_options.append(
                discord.SelectOption(
                    label= cl,
                    default= cl == "warrior"
                )
            )

        for gen in ["male", "female"]:
           gender_options.append(
                discord.SelectOption(
                    label = gen, default= gen == "male"
                )
            )

        for color in colors:
            color_options.append(
                discord.SelectOption(
                    label = color,
                    default = color == "blue"
                )
            )

        # rows: 1 gender, 2 class, 3 color

    @discord.ui.select(row = 1, options= gender_options)
    async def gender_callback(self, interaction: discord.Interaction, select: discord.ui.Select):
        if interaction.user.id != self.author_id:
            await interaction.response.send_message(f"This select can only be changed by <@{self.author_id}>")
            return

        self.selected_gender = select.values[0]
        await interaction.response.send_message(f"Changed gender to {self.selected_gender}", ephemeral= True)

    @discord.ui.select(row = 2, options= class_options)
    async def class_callback(self, interaction: discord.Interaction, select: discord.ui.Select):
        if interaction.user.id != self.author_id:
            await interaction.response.send_message(f"This select can only be changed by <@{self.author_id}>")
            return

        self.selected_class = select.values[0]
        await interaction.response.send_message(f"Changed class to {self.selected_class}", ephemeral= True)

    @discord.ui.select(row = 3, options= color_options)
    async def color_callback(self, interaction: discord.Interaction, select: discord.ui.Select):
        if interaction.user.id != self.author_id:
            await interaction.response.send_message(f"This select can only be changed by <@{self.author_id}>")
            return

        self.selected_color = select.values[0]
        await interaction.response.send_message(f"Changed color to {self.selected_color}", ephemeral= True)


    @discord.ui.button(row = 4, label= "Confirm", emoji="✅")
    async def button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.author_id:
            await interaction.response.send_message(f"This select can only be changed by <@{self.author_id}>")
            return

        self.client.world.create_player(
            str(self.author_id),
            self.selected_gender,
            self.selected_class,
            self.selected_color
        )

        await interaction.response.send_message("Character created!")
        self.stop()
