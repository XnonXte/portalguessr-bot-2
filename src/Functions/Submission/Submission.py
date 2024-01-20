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
from utils.bot.make_icon import make_icon
from utils.submission.get_color_by_status import get_color_by_status
from const import BOT_COLOR, MAX_AMOUNT, SUBMISSION_CHANNEL_ID


class Submission(commands.Cog):
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
        start="The starting index (one-based index).",
        amount=f"The total amount that needs to be displayed (max: {MAX_AMOUNT}",
    )
    async def submissions(
        self,
        ctx,
        submission_id: Optional[str] = "",
        status: Optional[Literal["Pending", "Accepted", "Rejected", "All"]] = "All",
        start: Optional[int] = 1,
        amount: Optional[int] = 10,
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
            submissions = (
                await read_submission_by_status(status.lower())
                if status != "All"
                else await read_submission()
            )
            submissions_length = len(submissions)

            if amount > MAX_AMOUNT:
                await ctx.send(
                    f"Amount value can't exceed {MAX_AMOUNT}!",
                    ephemeral=True,
                )

                return
            elif amount <= 0:
                await ctx.send(
                    "Amount value can't be less than or equal to 0!", ephemeral=True
                )

                return

            if submissions_length != 0:
                if start > submissions_length:
                    await ctx.send(
                        f"Start value cannot exceed {submissions_length}!",
                        ephemeral=True,
                    )

                    return
                elif start <= 0:
                    await ctx.send(
                        "Starting index cannot be less than or equal to 0!",
                        ephemeral=True,
                    )

                    return

            adjusted_amount = (
                (start + amount) - 1
                if not start + amount > submissions_length
                else submissions_length
            )
            adjusted_end_index = (
                adjusted_amount if start != submissions_length else adjusted_amount + 1
            )
            submissions_reversed = submissions[::-1]
            submissions_entry = []

            for index, submission in enumerate(submissions_reversed, start=1):
                submitter_mention = await get_user_mention(
                    self.bot, submission["submitter"]
                )

                entry_message = f"{index}. Submitted by {submitter_mention}, created at • <t:{submission['createdStamp']}:F>\n**{submission['status'].capitalize()}** status, **{submission['difficulty']}** difficulty | ID: `{submission['submissionId']}`"
                submissions_entry.append(entry_message)

            data_entry = submissions_entry[start - 1 : adjusted_end_index]
            data_entry_length = len(data_entry)
            embed_description = "\n\n".join(data_entry) or "Empty :("
            embed_title = (
                f"Submissions with {status.lower()} status"
                if status != "All"
                else "All Submissions"
            )

            embed = make_embed(
                embed_title,
                embed_description,
                BOT_COLOR,
            )
            embed.set_footer(
                text=f"Showing {data_entry_length} out of {submissions_length} total.",
                icon_url="attachment://icon.png",
            )

            await ctx.send(embed=embed, file=make_icon())


async def setup(bot):
    await bot.add_cog(Submission(bot))
