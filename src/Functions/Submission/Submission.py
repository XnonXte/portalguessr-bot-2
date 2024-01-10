from typing import Literal, Optional
from datetime import datetime

import discord
from discord.ext import commands
from discord import app_commands

from utils.imgbb.upload_image import upload_image
from utils.submission.submit import (
    submit_submission,
    read_one_submission,
    read_submission,
    read_submission_by_status,
)

from utils.owner.check_server import check_is_testing_server
from hooks.discord.use_discord import make_embed, get_user, get_user_mention
from utils.bot.utils import bot_make_icon
from utils.submission.utils import get_color_by_status
from const import BOT_COLOR, BOT_VERSION, TESTING_SERVER_ID


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

        allowed_image_types = ["png", "jpeg", "jpg", "webp"]
        file_extension = image.filename.split(".")[-1].lower()

        if file_extension not in allowed_image_types:
            await ctx.send("Image type not supported!", ephemeral=True)

            return

        await ctx.defer()

        uploaded_image_url = await upload_image(image.url, image.filename)
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
            file=bot_make_icon(),
        )

    @commands.hybrid_command(
        name="submissions", description="Checks submissions status."
    )
    @app_commands.describe(
        submission_id="Shows the detail for a specific submission with its ID.",
        status="Searches submissions by their status (defaults to 'Pending').",
    )
    async def submissions(
        self,
        ctx,
        submission_id: Optional[str] = "",
        status: Optional[Literal["Pending", "Accepted", "Rejected", "All"]] = "Pending",
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

                await ctx.send(embed=embed, file=bot_make_icon())
        elif status in ["Pending", "Accepted", "Rejected"]:
            submissions = await read_submission_by_status(status.lower())
            submissions_reversed = submissions[::-1]
            submissions_entry = []

            for index, submission in enumerate(submissions_reversed, start=1):
                submitter_mention = await get_user_mention(
                    self.bot, submission["submitter"]
                )
                submissions_entry.append(
                    f"{index}. Submitted by {submitter_mention}, created at • <t:{submission['createdStamp']}:F>\n**{submission['status'].capitalize()}** status, **{submission['difficulty']}** difficulty | ID: `{submission['submissionId']}`"
                )

            embed = make_embed(
                f"Submissions with {status.lower()} status",
                "\n\n".join(submissions_entry) or "Empty :(",
                BOT_COLOR,
            )
            embed.set_footer(
                text=f"PortalGuessr {BOT_VERSION}", icon_url="attachment://icon.png"
            )

            await ctx.send(embed=embed, file=bot_make_icon())
        else:
            submissions = await read_submission()
            submissions_reversed = submissions[::-1]
            submissions_entry = []

            for index, submission in enumerate(submissions_reversed, start=1):
                submitter_mention = await get_user_mention(
                    self.bot, submission["submitter"]
                )
                submissions_entry.append(
                    f"{index}. Submitted by {submitter_mention} - **{submission['status'].capitalize()}** status, **{submission['difficulty']}** difficulty\ncreated at • <t:{submission['createdStamp']}:F> | ID: `{submission['submissionId']}`"
                )

            embed = make_embed(
                "Submissions", "\n\n".join(submissions_entry) or "Empty :(", BOT_COLOR
            )
            embed.set_footer(
                text=f"PortalGuessr {BOT_VERSION}", icon_url="attachment://icon.png"
            )

            await ctx.send(embed=embed, file=bot_make_icon())


async def setup(bot):
    await bot.add_cog(Submission(bot))
