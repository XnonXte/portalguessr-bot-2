from discord.ext import commands

from hooks.discord.make_embed import make_embed
from utils.bot.make_icon import make_icon
from const import (
    GENERAL_COMMANDS,
    OWNER_COMMANDS,
    BOT_COLOR,
    BOT_PREFIX,
    DEFAULT_FOOTER_TEXT,
    GITHUB_URL,
)
from utils.help.buttons import HelpViews


class Help(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(
        name="help", description="Shows the available commands you can use."
    )
    async def help(self, ctx):
        general_commands_entry = [
            f"`{key}` - {GENERAL_COMMANDS[key]}" for key in GENERAL_COMMANDS
        ]
        owner_commands_entry = [
            f"`{key}` - {OWNER_COMMANDS[key]}" for key in OWNER_COMMANDS
        ]

        embed = make_embed(
            description=f"My command is available to both the prefix `{BOT_PREFIX}` command and the slash command!",
            color=BOT_COLOR,
        )
        embed.add_field(
            name="General Commands",
            value="\n".join(general_commands_entry),
            inline=False,
        )
        embed.add_field(
            name="Owner Commands",
            value="\n".join(owner_commands_entry),
            inline=False,
        )
        embed.set_author(
            name="About PortalGuessr", url=GITHUB_URL, icon_url="attachment://icon.png"
        )
        embed.set_footer(text=DEFAULT_FOOTER_TEXT, icon_url="attachment://icon.png")

        await ctx.send(embed=embed, file=make_icon(), view=HelpViews(), ephemeral=True)


async def setup(bot):
    await bot.add_cog(Help(bot))
