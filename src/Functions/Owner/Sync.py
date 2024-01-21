from typing import Optional, Literal

from discord.ext import commands


class Sync(commands.Cog):
    """Cog for Sync related command.

    Args:
        commands (commands.Bot): The bot's instance.
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def sync(self, ctx, scope: Optional[Literal["*", ".", "-"]] = "*"):
        if scope == "*":
            synced = await ctx.bot.tree.sync()
        elif scope == "-":
            ctx.bot.tree.clear_commands(guild=ctx.guild)
            await ctx.bot.tree.sync(guild=ctx.guild)
            synced = []
        else:
            ctx.bot.tree.copy_global_to(guild=ctx.guild)
            synced = await ctx.bot.tree.sync(guild=ctx.guild)

        await ctx.send(
            f"Synced {len(synced)} commands {'globally' if scope == '*' else 'to the current guild.'}"
        )


async def setup(bot):
    await bot.add_cog(Sync(bot))
