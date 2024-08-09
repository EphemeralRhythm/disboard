from utils.constants import COLOR_RED


class DiscordEvent:
    def __init__(self, author, channel, description, color=COLOR_RED):
        self.author_id = author
        self.channel_id = channel
        self.description = description
        self.color = color
