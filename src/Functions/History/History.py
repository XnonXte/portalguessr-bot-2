from typing import Optional

import discord
from discord.ext import commands
from discord import app_commands

from hooks.discord.use_discord import make_embed, make_file
from utils.guessr.history import read_history, read_one_history
from const import BOT_COLOR, BOT_VERSION


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
        if not history_id:
            history = await read_history()
            history_descending = reversed(history)
            history_entry = []

            for index, game in enumerate(history_descending, start=1):
                (
                    total,
                    solved,
                    timeout,
                    skipped,
                    mvp,
                    participators,
                    prompterUserId,
                    history_id,
                    difficulty,
                ) = (
                    game["total"],
                    game["solved"],
                    game["timeout"],
                    game["skipped"],
                    game["mvp"],
                    game["participators"],
                    game["prompterUserId"],
                    game["historyId"],
                    game["difficulty"],
                )

                mvp_mention = (
                    (await self.bot.fetch_user(int(mvp))).mention
                    if mvp != ""
                    else "None"
                )
                history_entry.append(
                    f"**{index}.** `{history_id}` - ***{solved}*** solved, ***{timeout}*** timed out, ***{skipped}*** skipped, ***{total}*** total, ***{difficulty}*** difficulty, {mvp_mention} MVP, {len(participators)} participated"
                )

            embed = make_embed("Game History", "\n".join(history_entry), BOT_COLOR)
            embed.set_footer(
                text=f"PortalGuessr has been played {len(history)} times!",
                icon_url="attachment://icon.png",
            )
            icon = make_file("./src/assets/icon.png", "icon.png")

            await ctx.send(embed=embed, file=icon)

            return

        game = await read_one_history(history_id)
        if not game:
            await ctx.send(
                f"Game with ID `{history_id}` does not exist in the leaderboard!",
                ephemeral=True,
            )

            return

        (
            total,
            solved,
            timeout,
            skipped,
            mvp,
            participators,
            prompterUserId,
            history_id,
            difficulty,
            finished_at,
        ) = (
            game["total"],
            game["solved"],
            game["timeout"],
            game["skipped"],
            game["mvp"],
            game["participators"],
            game["prompterUserId"],
            game["historyId"],
            game["difficulty"],
            game["createdStamp"],
        )

        mvp_mention = (await self.bot.fetch_user(int(mvp))).mention
        prompter = await self.bot.fetch_user(int(prompterUserId))

        embed = make_embed(
            None,
            f"Details for `{history_id}` game",
            BOT_COLOR,
        )
        embed.add_field(name="Solved", value=solved)
        embed.add_field(name="Timeout", value=timeout)
        embed.add_field(name="Skipped", value=skipped)
        embed.add_field(name="Total", value=total)
        embed.add_field(name="Difficulty", value=difficulty)
        embed.add_field(name="MVP", value=mvp_mention)
        embed.add_field(name="Participated", value=len(participators))
        embed.add_field(name="Finished at", value=f"<t:{finished_at}:f>")

        embed.set_footer(
            text=f"PortalGuessr 2 {BOT_VERSION}", icon_url="attachment://icon.png"
        )
        embed.set_author(
            name=f"Started by {prompter.name}", icon_url=prompter.avatar.url
        )

        icon = make_file("./src/assets/icon.png", "icon.png")

        await ctx.send(embed=embed, file=icon)


async def setup(bot):
    await bot.add_cog(History(bot))
