from typing import Optional

import discord
from discord.ext import commands
from discord import app_commands

from hooks.discord.use_discord import make_embed
from utils.guessr.lb import add_score, remove_score
from utils.owner.check_id import check_is_owner
from utils.submission.submit import update_submission, accept_submission
from const import (
    OWNER_USER_ID,
    BOT_COLOR,
    DEFAULT_FOOTER_TEXT,
)
from utils.bot.utils import bot_make_icon


class MyCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(
        name="lb_add",
        description="Adds a new stats to the leaderboard (owner only command).",
    )
    @app_commands.describe(
        user_id="A valid user ID on Discord.",
        easy_count="The number of easy guessrs.",
        medium_count="The number of medium guessrs.",
        hard_count="The number of hard guessrs.",
        very_hard_count="The number of very hard guessrs.",
    )
    async def lb_add(
        self,
        ctx,
        user_id: str,
        easy_count: int,
        medium_count: int,
        hard_count: int,
        very_hard_count: int,
    ):
        await check_is_owner(ctx.author.id, OWNER_USER_ID)
        await ctx.defer()

        data = {
            "scores": {
                "Easy": easy_count,
                "Medium": medium_count,
                "Hard": hard_count,
                "Very Hard": very_hard_count,
            }
        }

        try:
            result = await add_score(user_id, data)

            user_mention = (await self.bot.fetch_user(int(user_id))).mention
            embed = make_embed(
                "Success!", f"Stats for {user_mention} has been created!", BOT_COLOR
            )
            embed.set_footer(
                text=f"Database ID: {result['_id']}", icon_url="attachment://icon.png"
            )

            await ctx.send(embed=embed, file=bot_make_icon())
        except Exception as e:
            await ctx.send(
                embed=make_embed(
                    "Failed while adding user stats to the leaderboard",
                    f"```{e}```",
                    "#ff0000",
                )
            )

    @commands.hybrid_command(
        name="lb_rm",
        description="Removes an existing stats from the leaderboard (owner only command).",
    )
    @app_commands.describe(user_id="The target's user ID on Discord.")
    async def lb_rm(self, ctx, user_id: str):
        await check_is_owner(ctx.author.id, OWNER_USER_ID)
        await ctx.defer()

        try:
            result = await remove_score(int(user_id))
            if result["deletedCount"] == 0:
                await ctx.send(
                    f"Not found stats with user ID: {user_id}!", ephemeral=True
                )

                return

            user_mention = (await self.bot.fetch_user(int(user_id))).mention

            embed = make_embed(
                "Success!",
                f"{user_mention} stats in the leaderboard has been removed!!",
                BOT_COLOR,
            )
            embed.set_footer(text=DEFAULT_FOOTER_TEXT, icon_url="attachment://icon.png")

            await ctx.send(embed=embed, file=bot_make_icon())
        except Exception as e:
            await ctx.send(
                embed=make_embed(
                    "Failed while removing user stats from the leaderboard",
                    f"```{e}```",
                    "#ff0000",
                )
            )

    @commands.hybrid_command(
        name="reject", description="Rejects a pending submission (owner only command)."
    )
    @app_commands.describe(
        submission_id="Target a submission to reject with its ID.",
        reason="The reason for rejection.",
    )
    async def reject(
        self, ctx, submission_id: str, reason: Optional[str] = "No reason specified."
    ):
        await check_is_owner(ctx.author.id, OWNER_USER_ID)
        await ctx.defer()

        try:
            result = await update_submission(submission_id, "rejected")

            if not result:
                await ctx.send(
                    f"Not found submission ID: {submission_id}!",
                    ephemeral=True,
                )

                return

            submitter = result["submitter"]
            submitter_mention = (await self.bot.fetch_user(int(submitter))).mention

            embed = make_embed(None, f"Submission ID: `{submission_id}`", BOT_COLOR)
            embed.add_field(name="Reason", value=reason)
            embed.set_footer(text=DEFAULT_FOOTER_TEXT, icon_url="attachment://icon.png")

            await ctx.send(
                f"{submitter_mention} your submission has been rejected! Better luck next time!",
                embed=embed,
                file=bot_make_icon(),
            )
        except Exception as e:
            await ctx.send(
                embed=make_embed(
                    "Failed while rejecting a submission!",
                    f"```{e}```",
                    "#ff0000",
                )
            )

    @commands.hybrid_command(
        name="accept", description="Accepts a pending submission (owner only command)."
    )
    @app_commands.describe(submission_id="Target a submission to accept with its ID.")
    async def accept(self, ctx, submission_id: str):
        await check_is_owner(ctx.author.id, OWNER_USER_ID)
        await ctx.defer()

        try:
            result = await accept_submission(submission_id)

            submitter, chamber_id = result["submitter"], result["fileId"]
            submitter_mention = (await self.bot.fetch_user(int(submitter))).mention

            embed = make_embed(None, f"Submission ID: `{submission_id}`", BOT_COLOR)
            embed.add_field(name="Chamber ID", value=chamber_id)
            embed.set_footer(text=DEFAULT_FOOTER_TEXT, icon_url="attachment://icon.png")

            await ctx.send(
                f"{submitter_mention} your submission has been accepted! Thank you for your contribution!",
                embed=embed,
                file=bot_make_icon(),
            )
        except Exception as e:
            await ctx.send(
                embed=make_embed(
                    "Failed while accepting a submission!",
                    f"```{e}```",
                    "#ff0000",
                )
            )


async def setup(bot):
    await bot.add_cog(MyCog(bot))
