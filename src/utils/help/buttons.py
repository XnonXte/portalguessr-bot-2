import discord
from config import DISCORD_INVITE, INVITE_URL


class HelpViews(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(
            discord.ui.Button(label="Discord", url=DISCORD_INVITE),
        )
        self.add_item(discord.ui.Button(label="Invite", url=INVITE_URL))
