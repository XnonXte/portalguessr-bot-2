import os

import discord
from discord.ext import commands
import dotenv

from misc.replit import keep_alive

dotenv.load_dotenv("../.env")

bot_token = os.getenv("BOT_TOKEN")
prefix = commands.when_mentioned_or("!p")
intents = discord.Intents.default()
intents.message_content = True


class PortalGuessr2(commands.Bot):
    async def setup_hook(self):
        for cog in os.listdir("./exts"):
            try:
                if cog.endswith(".py") and cog != "__init__.py":
                    await self.load_extension(f"exts.{cog[:-3]}")
            except Exception as e:
                print(e)


bot = PortalGuessr2(command_prefix=prefix, intents=intents)


@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}!")

    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.custom, name=f"Try !pguess or /guess"
        )
    )


keep_alive()

bot.run(bot_token)
