from discord.ext import commands

from utils.discord_utils import make_embed, make_file
from const import LIST_TEXT_MAP, BOT_COLOR, BOT_VERSION


class Help(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(
        name="list", description="Shows the available command you can use."
    )
    async def list(self, ctx: commands.Context):
        command_entry = []
        for command in LIST_TEXT_MAP:
            command_entry.append(f"`{command}` - {LIST_TEXT_MAP[command]}")

        embed = make_embed("Available Commands", "\n".join(command_entry), BOT_COLOR)
        embed.set_footer(
            text=f"PortalGuessr {BOT_VERSION}", icon_url="attachment://icon.png"
        )

        await ctx.send(embed=embed, file=make_file("./src/assets/icon.png", "icon.png"))


async def setup(bot):
    await bot.add_cog(Help(bot))
