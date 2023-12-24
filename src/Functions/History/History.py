from typing import Optional

import discord
from discord.ext import commands
from discord import app_commands

from hooks.discord.use_discord import make_embed
from utils.guessr.history import read_history, read_one_history
from const import BOT_COLOR, DEFAULT_FOOTER_TEXT
from utils.bot.utils import bot_make_icon


class History(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(
        name="history", description="Checks recent guessrs history."
    )
    @app_commands.describe(
        history_id="Targets a specific game from history with its ID."
    )
    async def history(self, ctx: commands.Context, history_id: Optional[str]):
        await ctx.defer()

        if history_id:
            game = await read_one_history(history_id)

            if not game:
                await ctx.send(
                    f"Game ID: `{history_id}` does not exist in the leaderboard!",
                    ephemeral=True,
                )
                return

            mvp = await self.bot.fetch_user(int(game["mvp"]))
            prompter = await self.bot.fetch_user(int(game["prompterUserId"]))

            embed = make_embed(
                None,
                f"`{game['historyId']}` game details",
                BOT_COLOR,
            )
            embed.add_field(name="Solved", value=game["solved"])
            embed.add_field(name="Timed out", value=game["timeout"])
            embed.add_field(name="Skipped", value=game["skipped"])
            embed.add_field(name="Total", value=game["total"])
            embed.add_field(name="Difficulty", value=game["difficulty"])
            embed.add_field(name="MVP", value=mvp.mention if mvp else "None")
            embed.add_field(name="Participated", value=len(game["participators"]))
            embed.add_field(name="Finished at", value=f"<t:{game['createdStamp']}:f>")

            embed.set_footer(text=DEFAULT_FOOTER_TEXT, icon_url="attachment://icon.png")
            embed.set_author(
                name=f"Game started by {prompter.name}", icon_url=prompter.avatar.url
            )

            await ctx.send(embed=embed, file=bot_make_icon())

            return

        history = await read_history()
        history_entry = []

        for index, game in enumerate(reversed(history), start=1):
            history_entry.append(
                f"{index}. `{game['historyId']}` - **{game['solved']}** solved, **{game['timeout']}** timed out, **{game['skipped']}** skipped, **{game['total']}** total, **{game['difficulty']}** difficulty"
            )

        embed = make_embed(
            "Game History", "\n".join(history_entry) or "Empty :(", BOT_COLOR
        )
        embed.set_footer(
            text=f"PortalGuessr has been played {len(history)} times!",
            icon_url="attachment://icon.png",
        )

        await ctx.send(embed=embed, file=bot_make_icon())


async def setup(bot):
    await bot.add_cog(History(bot))
