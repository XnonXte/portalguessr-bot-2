from typing import Optional
from datetime import datetime

from discord.ext import commands
from discord import app_commands

from hooks.discord.make_embed import make_embed
from hooks.discord.get_user_mention import get_user_mention
from hooks.discord.get_user import get_user
from utils.submission.submission import (
    read_submission_by_status,
    update_submission_status,
    accept_submission,
)
from utils.owner.check_id import check_is_owner
from utils.submission.get_color_by_status import get_color_by_status
from utils.bot.make_icon import make_icon
from const import DEFAULT_FOOTER_TEXT, BOT_COLOR


class Review(commands.Cog):
    """Cog for review related command.

    Args:
        commands (commands.Bot): The bot's instance.
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(
        name="review",
        description="Starts a review session for pending submissions (owner only command).",
    )
    @app_commands.describe(
        limit="The amount of submissions you want to review (defaults to 10)."
    )
    async def review(self, ctx, limit: Optional[int] = 10):
        check_is_owner(ctx.author.id)

        if limit <= 0:
            await ctx.send(
                "The amount value can't be less than or equal to 0!", ephemeral=True
            )

            return

        await ctx.defer()

        submissions = await read_submission_by_status("pending", 1, limit)

        for index, submission in enumerate(submissions, start=1):
            submitter = await get_user(self.bot, submission["submitter"])
            submitter_name = submitter.name if submitter != None else "N/A"
            submitter_avatar = (
                submitter.avatar.url if submitter != None else "attachment://icon.png"
            )
            submitter_mention = await get_user_mention(
                self.bot, submission["submitter"]
            )

            formatted_time = datetime.fromtimestamp(
                submission["createdStamp"]
            ).strftime("%B %d, %Y %I:%M %p")

            embed = make_embed(
                description=f"Submitted by {submitter_mention}",
                color=get_color_by_status(submission["status"]),
            )
            embed.add_field(name="Status", value=submission["status"].capitalize())
            embed.add_field(name="Difficulty", value=submission["difficulty"])
            embed.add_field(name="Answer", value=f"||{submission['answer']}||")
            embed.set_image(url=submission["url"])
            embed.set_author(name=submitter_name, icon_url=submitter_avatar)
            embed.set_footer(
                text=f"Submission {index} of {len(submissions)} - ID: {submission['submissionId']} | Created at • {formatted_time}",
                icon_url="attachment://icon.png",
            )

            await ctx.send(embed=embed, file=make_icon())

            try:
                response = await self.bot.wait_for(
                    "message",
                    check=lambda m: m.author.id == ctx.author.id
                    and m.channel.id == ctx.channel.id
                    and m.content.lower() in ["accept", "reject", "skip", "stop"],
                )

                if response.content.lower() == "accept":
                    result = await accept_submission(submission["submissionId"])

                    embed = make_embed(
                        "Submission Accepted!",
                        color=BOT_COLOR,
                    )
                    embed.add_field(
                        name="Submission ID",
                        value=submission["submissionId"],
                        inline=False,
                    )
                    embed.add_field(
                        name="Chamber ID", value=result["fileId"], inline=False
                    )
                    embed.set_footer(
                        text=DEFAULT_FOOTER_TEXT, icon_url="attachment://icon.png"
                    )

                    await ctx.send(
                        embed=embed,
                        file=make_icon(),
                    )
                elif response.content.lower() == "reject":
                    await ctx.send("What's the reason for rejecting?")

                    reason = await self.bot.wait_for(
                        "message",
                        check=lambda m: m.author.id == ctx.author.id
                        and m.channel.id == ctx.channel.id,
                    )

                    result = await update_submission_status(
                        submission["submissionId"], "rejected"
                    )

                    embed = make_embed(
                        "Submission Rejected!",
                        color=BOT_COLOR,
                    )
                    embed.add_field(
                        name="Submission ID", value=submission["submissionId"]
                    )
                    embed.add_field(name="Reason", value=reason.content)
                    embed.set_footer(
                        text=DEFAULT_FOOTER_TEXT, icon_url="attachment://icon.png"
                    )

                    await ctx.send(
                        embed=embed,
                        file=make_icon(),
                    )
                elif response.content.lower() == "skip":
                    await ctx.send(
                        embed=make_embed("Submission skipped!", color=BOT_COLOR)
                    )
                else:
                    await ctx.send(
                        embed=make_embed("Review session ended!", color=BOT_COLOR)
                    )

                    break
            except Exception as e:
                raise commands.CommandError(e)


async def setup(bot):
    await bot.add_cog(Review(bot))
