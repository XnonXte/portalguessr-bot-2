from typing import Literal, Optional
from datetime import datetime

import discord
from discord.ext import commands
from discord import app_commands

from utils.imgbb.upload_image import upload_image
from utils.submission.submission import (
    submit_submission,
    read_one_submission,
    read_submission,
    read_submission_by_status,
)

from utils.owner.check_server import check_is_testing_server
from hooks.discord.make_embed import make_embed
from hooks.discord.get_user_mention import get_user_mention
from hooks.discord.get_user import get_user
from hooks.python.use_enumerate import use_enumerate
from utils.bot.make_icon import make_icon
from utils.submission.get_color_by_status import get_color_by_status
from const import (
    BOT_COLOR,
    MAX_LIMIT,
    DEFAULT_LIMIT,
    SUBMISSION_CHANNEL_ID,
    AVAILABLE_CHAMBERS,
    AVAILABLE_DIFFICULTIES,
)


class Submission(commands.Cog):
    """Cog for submission related command.

    Args:
        commands (commands.Bot): The bot's instance.
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(
        name="submit", description="Submits a chamber for the chance of getting added."
    )
    @app_commands.describe(
        image="The image to submit (must be a valid image file!)",
        difficulty="The expected difficulty when guessing this image.",
        answer="The answer to the guessr (must be correct).",
    )
    async def submit(
        self,
        ctx,
        image: discord.Attachment,
        difficulty: AVAILABLE_DIFFICULTIES,
        answer: AVAILABLE_CHAMBERS,
    ):
        check_is_testing_server(ctx.guild.id)

        if ctx.channel.id != SUBMISSION_CHANNEL_ID:
            await ctx.send(
                f"This command is only permitted to be invoked in {ctx.guild.get_channel(SUBMISSION_CHANNEL_ID).mention}"
            )

        allowed_image_types = ["png", "jpeg", "jpg", "webp"]
        file_extension = image.filename.split(".")[-1].lower()

        if file_extension not in allowed_image_types:
            await ctx.send("Image type not supported!", ephemeral=True)

            return

        await ctx.defer()

        uploaded_image_url = await upload_image(image.url)
        submission_id = (
            await submit_submission(
                uploaded_image_url, difficulty, answer, str(ctx.author.id), ""
            )
        )["submissionId"]

        await ctx.send(
            embed=make_embed(
                "Success!",
                f"Your submission is required to be checked first before it gets added to the game, we will notify you when there's an updated. Thanks for contributing! {ctx.author.mention}",
                BOT_COLOR,
            ).set_footer(
                text=f"Submission ID: {submission_id}", icon_url="attachment://icon.png"
            ),
            file=make_icon(),
        )

    @commands.hybrid_command(
        name="submissions", description="Checks submissions status."
    )
    @app_commands.describe(
        submission_id="Shows the detail for a specific submission with its ID.",
        status="Searches submissions by their status (defaults to 'All').",
        skip="Skip to the given number (defaults to 1).",
        limit=f"The total amount that needs to be displayed (defaults to {DEFAULT_LIMIT}, {MAX_LIMIT} maximum)",
    )
    async def submissions(
        self,
        ctx,
        submission_id: Optional[str] = "",
        status: Optional[Literal["Pending", "Accepted", "Rejected", "All"]] = "All",
        skip: Optional[int] = 1,
        limit: Optional[int] = DEFAULT_LIMIT,
    ):
        await ctx.defer()

        if submission_id:
            submission = await read_one_submission(submission_id)

            if not submission:
                raise commands.BadArgument(
                    f"{submission_id} is not a valid submission ID!"
                )
            else:
                submitter = await get_user(self.bot, submission["submitter"])
                submitter_name = submitter.name if submitter != None else "N/A"
                submitter_avatar = (
                    submitter.avatar.url
                    if submitter != None
                    else "attachment://icon.png"
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
                    text=f"ID: {submission_id} | Created at • {formatted_time}",
                    icon_url="attachment://icon.png",
                )

                await ctx.send(embed=embed, file=make_icon())
        else:
            if limit > MAX_LIMIT:
                await ctx.send(
                    f"Exceeded the maximum value for amount! The maximum value is {MAX_LIMIT}",
                    ephemeral=True,
                )

                return
            elif limit <= 0:
                await ctx.send(
                    "The amount value can't be less than or equal to 0!", ephemeral=True
                )

                return

            if skip <= 0:
                await ctx.send(
                    "The starting number can't be less than or equal to 0!",
                    ephemeral=True,
                )

                return

            submissions = (
                await read_submission_by_status(status.lower(), skip, limit)
                if status != "All"
                else await read_submission(skip, limit)
            )
            submissions_length = len(submissions)

            submissions_entry = []

            async def callback(index, item):
                submitter_mention = await get_user_mention(self.bot, item["submitter"])
                entry_message = f"{index}. Submitted by {submitter_mention}, created at • <t:{item['createdStamp']}:F>\n**{item['status'].capitalize()}** status, **{item['difficulty']}** difficulty | ID: `{item['submissionId']}`"

                submissions_entry.append(entry_message)

            await use_enumerate(submissions, callback, skip)

            embed_description = "\n\n".join(submissions_entry) or "Empty :("
            embed_title = (
                f"Submissions with {status.lower()} status"
                if status != "All"
                else "All Submissions"
            )
            embed_footer = (
                f"Showing {submissions_length} results | Skipping from {skip}"
                if skip != 1
                else f"Showing {submissions_length} results "
            )
            embed = make_embed(
                embed_title,
                embed_description,
                BOT_COLOR,
            )
            embed.set_footer(
                text=embed_footer,
                icon_url="attachment://icon.png",
            )

            await ctx.send(embed=embed, file=make_icon())


async def setup(bot):
    await bot.add_cog(Submission(bot))
