from typing import Optional, Literal
from discord.ext import commands
from discord import app_commands
from hooks.discord.make_embed import make_embed
from hooks.discord.get_user_mention import get_user_mention
from utils.game.lb import add_statistic, remove_statistic
from utils.owner.check_id import check_is_owner
from utils.submission.submission import (
    update_submission_status,
    update_submission,
    accept_submission,
)
from utils.bot.make_icon import make_icon
from config import BOT_ACCENT_COLOR, BOT_FOOTER_TEXT


class Owner(commands.Cog):
    """Cog for owner related command.

    Args:
        commands (commands.Bot): The bot's instance.
    """

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
        check_is_owner(ctx.author.id)
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
            result = await add_statistic(user_id, data)
            user_mention = await get_user_mention(self.bot, user_id)

            embed = make_embed(
                "Success!",
                f"Stats for {user_mention} has been created!",
                BOT_ACCENT_COLOR,
            )
            embed.set_footer(
                text=f"Database ID: {result['_id']}", icon_url="attachment://icon.png"
            )
            await ctx.send(embed=embed, file=make_icon())
        except Exception as e:
            raise commands.CommandError(e)

    @commands.hybrid_command(
        name="lb_rm",
        description="Removes an existing stats from the leaderboard (owner only command).",
    )
    @app_commands.describe(user_id="The target's user ID on Discord.")
    async def lb_rm(self, ctx, user_id: str):
        check_is_owner(ctx.author.id)
        await ctx.defer()
        try:
            result = await remove_statistic(int(user_id))
            if result["deletedCount"] == 0:
                raise commands.UserNotFound(user_id)
            else:
                user_mention = await get_user_mention(self.bot, user_id)
                embed = make_embed(
                    "Success!",
                    f"{user_mention} stats in the leaderboard has been removed!!",
                    BOT_ACCENT_COLOR,
                )
                embed.set_footer(text=BOT_FOOTER_TEXT, icon_url="attachment://icon.png")
                await ctx.send(embed=embed, file=make_icon())
        except Exception as e:
            raise commands.CommandError(e)

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
        check_is_owner(ctx.author.id)
        await ctx.defer()
        try:
            result = await update_submission_status(submission_id, "rejected")
            if result == None:
                raise commands.BadArgument(
                    f"{submission_id} is not a valid submission ID!"
                )
            else:
                embed = make_embed(
                    "Submission Rejected!",
                    color=BOT_ACCENT_COLOR,
                )
                embed.add_field(name="Submission ID", value=result["submissionId"])
                embed.add_field(name="Reason", value=reason.content)
                embed.set_footer(text=BOT_FOOTER_TEXT, icon_url="attachment://icon.png")
                await ctx.send(
                    embed=embed,
                    file=make_icon(),
                )
        except Exception as e:
            raise commands.CommandError(e)

    @commands.hybrid_command(
        name="accept", description="Accepts a pending submission (owner only command)."
    )
    @app_commands.describe(submission_id="Target a submission to accept with its ID.")
    async def accept(self, ctx, submission_id: str):
        check_is_owner(ctx.author.id)
        await ctx.defer()
        try:
            result = await accept_submission(submission_id)
            embed = make_embed(
                "Submission Accepted!",
                color=BOT_ACCENT_COLOR,
            )
            embed.add_field(
                name="Submission ID",
                value=result["submissionId"],
                inline=False,
            )
            embed.add_field(name="Chamber ID", value=result["fileId"], inline=False)
            embed.set_footer(text=BOT_FOOTER_TEXT, icon_url="attachment://icon.png")

            await ctx.send(
                embed=embed,
                file=make_icon(),
            )
        except Exception as e:
            raise commands.CommandError(e)

    @commands.hybrid_command(
        name="edit", description="Edit a submission (owner only command)."
    )
    @app_commands.describe(submission_id="Target a submission to edit with its ID.")
    async def edit(
        self,
        ctx,
        submission_id: str,
        difficulty: Literal["Easy", "Medium", "Hard", "Very Hard"],
        answer: Literal[
            "00",
            "01",
            "02",
            "03",
            "04",
            "05",
            "06",
            "07",
            "08",
            "09",
            "10",
            "11",
            "12",
            "13",
            "14",
            "15",
            "16",
            "17",
            "18",
            "19",
            "e00",
            "e01",
            "e02",
        ],
    ):
        check_is_owner(ctx.author.id)
        await ctx.defer()
        try:
            await update_submission(submission_id, difficulty, answer)
            embed = make_embed(
                "Submission Updated!",
                f"Submission with ID {submission_id} has been updated!",
                BOT_ACCENT_COLOR,
            )
            embed.set_footer(text=BOT_FOOTER_TEXT, icon_url="attachment://icon.png")
            await ctx.send(
                embed=embed,
                file=make_icon(),
            )
        except Exception as e:
            raise commands.CommandError(e)


async def setup(bot):
    await bot.add_cog(Owner(bot))
