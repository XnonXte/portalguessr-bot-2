import discord
from discord.ext import commands
from discord import app_commands


class Submission(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


async def setup(bot):
    await bot.add_cog(Submission(bot))
