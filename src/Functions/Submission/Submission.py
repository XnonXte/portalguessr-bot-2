from typing import Literal, Optional

import discord
from discord.ext import commands
from discord import app_commands

from utils.imgbb.upload_image import upload_image
from utils.submission.submit import (
    submit_submission,
    read_one_submission,
    read_submission,
)
from utils.guessr.utils import get_color
from hooks.discord.use_discord import make_embed, make_file
from const import BOT_COLOR, BOT_VERSION


class Submission(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(
        name="submit", description="Submits a chamber for the chance of getting added"
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
        allowed_image_types = ["png", "jpeg", "jpg", "webp"]
        file_extension = image.filename.split(".")[-1].lower()

        if file_extension not in allowed_image_types:
            await ctx.send("Image type not supported!", ephemeral=True)

            return

        await ctx.defer()

        uploaded_image_url = upload_image(image.url, image.filename)
        submission_id = (
            await submit_submission(
                uploaded_image_url, difficulty, answer, str(ctx.author.id), ""
            )
        )["submissionId"]

        icon = make_file("./src/assets/icon.png", "icon.png")

        await ctx.send(
            embed=make_embed(
                "Success!",
                f"Your submission is required to be checked first before it gets added to the game, we will notify you when there's an updated. Thanks for contributing! {ctx.author.mention}",
                BOT_COLOR,
            ).set_footer(text=f"ID: {submission_id}", icon_url="attachment://icon.png"),
            file=icon,
        )

    @commands.hybrid_command(
        name="status", description="Checks the status of the current submissions."
    )
    @app_commands.describe(
        submission_id="Shows the detail for a specific submission with its ID."
    )
    async def status(self, ctx, submission_id: Optional[str] = ""):
        if submission_id:
            target_submission = await read_one_submission(submission_id)
            if not target_submission:
                await ctx.send(
                    f"Submission with ID `{submission_id}` does not exist in the database!",
                    ephemeral=True,
                )

                return

            status = target_submission["status"]
            difficulty = target_submission["difficulty"]
            submitter = target_submission["submitter"]
            url = target_submission["url"]
            submitted_at = target_submission["createdStamp"]

            submitter_mention = (await self.bot.fetch_user(int(submitter))).mention

            embed = make_embed(
                None,
                f"Details for submission with ID: `{submission_id}`",
                get_color(difficulty),
            )
            embed.add_field(name="Status", value=status.capitalize())
            embed.add_field(name="Difficulty", value=difficulty)
            embed.add_field(name="Submitted by", value=submitter_mention)
            embed.add_field(name="Submitted at", value=f"<t:{submitted_at}:f>")
            embed.set_image(url=url)
            embed.set_footer(
                text=f"PortalGuessr {BOT_VERSION}", icon_url="attachment://icon.png"
            )

            icon = make_file("./src/assets/icon.png", "icon.png")

            await ctx.send(embed=embed, file=icon)

            return

        submissions = await read_submission()
        submissions_descending = reversed(submissions)
        submissions_entry = []

        for index, submission in enumerate(submissions_descending, start=1):
            status = submission["status"]
            difficulty = submission["difficulty"]
            submitter = submission["submitter"]
            url = submission["url"]
            submission_id = submission["submissionId"]
            submitted_at = submission["createdStamp"]

            submitter_mention = (await self.bot.fetch_user(int(submitter))).mention

            submissions_entry.append(
                f"**{index}.** `{submission_id}` - ***{status.capitalize()}*** status, ***{difficulty}*** difficulty | Submitted by {submitter_mention} at <t:{submitted_at}:f>"
            )

        embed = make_embed(
            "Submissions Status", "\n".join(submissions_entry), BOT_COLOR
        )
        embed.set_footer(
            text=f"PortalGuessr {BOT_VERSION}", icon_url="attachment://icon.png"
        )

        icon = make_file("./src/assets/icon.png", "icon.png")

        await ctx.send(embed=embed, file=icon)


async def setup(bot):
    await bot.add_cog(Submission(bot))
