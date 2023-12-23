from discord.ext import commands

from hooks.discord.use_discord import make_embed
from const import (
    GENERAL_COMMANDS,
    OWNER_COMMANDS,
    BOT_COLOR,
    DEFAULT_FOOTER_TEXT,
)
from utils.bot.utils import bot_make_icon


class Help(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(
        name="help", description="Shows the available commands you can use."
    )
    async def help(self, ctx: commands.Context):
        general_commands_entry = [
            f"`{key}` - {GENERAL_COMMANDS[key]}" for key in GENERAL_COMMANDS
        ]
        owner_commands_entry = [
            f"`{key}` - {OWNER_COMMANDS[key]}" for key in OWNER_COMMANDS
        ]

        embed = make_embed(
            "PortalGuessr Help",
            f"Some command might now work properly when invoked with the prefix command, it's recommended to use the slash command instead!",
            BOT_COLOR,
        )
        embed.add_field(
            name="General Commands",
            value="\n".join(general_commands_entry),
            inline=False,
        )
        embed.add_field(
            name="Owner Only Commands",
            value="\n".join(owner_commands_entry),
            inline=False,
        )
        embed.set_footer(text=DEFAULT_FOOTER_TEXT, icon_url="attachment://icon.png")

        await ctx.send(embed=embed, file=bot_make_icon(), ephemeral=True)


async def setup(bot):
    await bot.add_cog(Help(bot))
