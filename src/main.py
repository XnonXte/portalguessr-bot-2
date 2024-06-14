import os
import discord
from discord.ext import commands
from config import TOKEN, BOT_PREFIX, BOT_STATUS


class PortalGuessr2(commands.Bot):
    BOT_INTENTS = discord.Intents.default()
    BOT_INTENTS.message_content = True
    BOT_ACTIVITY = discord.Activity(
        type=discord.ActivityType.playing, name=f"{BOT_PREFIX} | {BOT_STATUS}"
    )
    BOT_STATUS = discord.Status.do_not_disturb

    def __init__(self):
        super().__init__(
            command_prefix=BOT_PREFIX,
            intents=self.BOT_INTENTS,
            help_command=None,
            activity=self.BOT_ACTIVITY,
            status=BOT_STATUS,
        )

    async def setup_hook(self):
        for function in os.listdir("./src/Functions"):
            for cog in os.listdir(f"./src/Functions/{function}"):
                if cog.endswith(".py") and cog != "__init__.py":
                    await self.load_extension(
                        f"Functions.{function}.{cog[:-3]}"
                    )  # Excluding .py


bot = PortalGuessr2()


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}! - Inside {len(bot.guilds)} server(s)")


if __name__ == "__main__":
    bot.run(TOKEN)
