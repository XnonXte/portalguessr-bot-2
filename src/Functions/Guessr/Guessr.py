import asyncio
import time
from typing import Literal, Optional

import discord
from discord import app_commands
from discord.ext import commands

from utils.guessr_scores import update_user_score
from utils.guessr_chambers_req import (
    guessr_get_chambers,
    guessr_get_random_chambers,
)
from utils.guessr_utils import (
    guessr_find_mvp,
    guessr_get_color,
    guessr_get_timeout,
)
from utils.discord_utils import make_embed, make_file
from const import BOT_COLOR, GUESSR_CHAMBERS

running_channels = []


class Guessr(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(name="guess", description="Starts the game.")
    @app_commands.describe(
        difficulty="The desired difficulty (leave blank to keep it random).",
        rounds="The amount of rounds in a session.",
    )
    async def guess(
        self,
        ctx: commands.Context,
        difficulty: Optional[Literal["Easy", "Medium", "Hard", "Very Hard"]] = "Random",
        rounds: Optional[int] = 10,
    ):
        global running_channels

        def is_valid(message: discord.Message):
            # Check the validity of the responder's message.
            return (
                message.guild.id == ctx.guild.id
                and message.channel.id == ctx.channel.id
                and message.content.lower() in GUESSR_CHAMBERS + ["skip", "stop"]
            )

        # Defer the command a little bit.
        await ctx.defer()

        if rounds <= 0:
            await ctx.send(
                "The amount of rounds must be higher than 0!",
                ephemeral=True,
                delete_after=5,
            )
            return

        if ctx.channel.id in running_channels:
            await ctx.send(
                f"A game is already running in {ctx.channel.mention}. Please wait for it to finish or start another instance in a different channel!",
                ephemeral=True,
                delete_after=10,
            )
            return

        running_channels.append(ctx.channel.id)

        session_data = {
            # Data per session.
            "solved_guessr": 0,
            "unsolved_guessr": 0,
            "session_skipped": 0,
            "session_users_participated": [],
            "session_users_correct": [],
            "session_stopped": False,
        }

        try:
            guessr_chambers = (
                await guessr_get_chambers(rounds, difficulty)
                if difficulty != "Random"
                else await guessr_get_random_chambers(rounds)
            )

        except Exception as e:
            await ctx.send(
                f"An error occurred! Error: {e}", ephemeral=True, delete_after=5
            )

        for i in range(rounds):
            guessr_chamber = guessr_chambers[i]

            guessr_image_url = guessr_chamber["url"]
            guessr_answer = guessr_chamber["answer"]
            guessr_difficulty = guessr_chamber["difficulty"]

            guessr_start_time = time.time()
            guessr_elapsed_time = 0
            guessr_timeout = guessr_get_timeout(guessr_difficulty)

            guessr_data = {
                # Data per guessr.
                "guessr_user_id_have_answered": [],
                "guessr_answer_count": 0,
                "guessr_answer_count_max": 5,
            }

            guessr_embed = make_embed(
                title="Guess the chamber!",
                color=guessr_get_color(guessr_difficulty),
            )
            guessr_embed.set_image(url=guessr_image_url)
            guessr_embed.set_footer(
                text=f"Round {i + 1} of {rounds} - skip | stop",
                icon_url="attachment://icon.png",
            )

            if i == 0:
                await ctx.send(
                    embed=guessr_embed,
                    file=make_file("./src/assets/icon.png", "icon.png"),
                )
            else:
                await ctx.channel.send(
                    embed=guessr_embed,
                    file=make_file("./src/assets/icon.png", "icon.png"),
                )

            while True:
                try:
                    res = await self.bot.wait_for(
                        "message",
                        check=is_valid,
                        timeout=guessr_timeout - guessr_elapsed_time,
                    )

                    res_lower = res.content.lower()
                    res_id = res.author.id
                    res_name = ctx.author.name

                    if res_lower == "skip" or res_lower == "stop":
                        if res_id != ctx.author.id:
                            # Responder must be the prompter.
                            await res.reply(
                                embed=make_embed(
                                    title="You're not allowed to use this command!",
                                    description="Only the user prompted this guessr is eligible to use this command.",
                                    color=BOT_COLOR,
                                ),
                                delete_after=3,
                                mention_author=False,
                            )

                            continue

                        if res_lower == "skip":
                            session_data["session_skipped"] += 1

                            await res.reply(
                                embed=make_embed(
                                    title="Guessr Skipped!", color=BOT_COLOR
                                ),
                                mention_author=False,
                            )

                            break
                        elif res_lower == "stop":
                            session_data["session_stopped"] = True

                            await res.reply(
                                embed=make_embed(
                                    title="Guessr Stopped!", color=BOT_COLOR
                                ),
                                mention_author=False,
                            )

                            break
                    if (
                        # If the responder has responded once.
                        res_id
                        in guessr_data["guessr_user_id_have_answered"]
                    ):
                        await res.reply(
                            embed=make_embed(
                                title="You have answered! Answer ignored.",
                                color=BOT_COLOR,
                            ),
                            delete_after=3,
                            mention_author=False,
                        )

                        continue

                    if res_name not in session_data["session_users_participated"]:
                        session_data["session_users_participated"].append(res_name)

                    guessr_data["guessr_user_id_have_answered"].append(res_id)
                    guessr_data["guessr_answer_count"] += 1

                    if res_lower == guessr_answer:
                        session_data["solved_guessr"] += 1
                        session_data["session_users_correct"].append(res_name)

                        await update_user_score(res_id, guessr_difficulty)
                        await res.add_reaction("✅")

                        break
                    else:
                        await res.add_reaction("❌")

                    if (
                        guessr_data["guessr_answer_count"]
                        >= guessr_data["guessr_answer_count_max"]
                    ):
                        # After 5 respondent.
                        await ctx.channel.send(
                            embed=make_embed(
                                title="Game Finished!",
                                description=f"5 users have attempted at guessing this chamber, but no one got it right!\nThe chamber is {guessr_answer}!",
                                color=BOT_COLOR,
                            )
                        )

                        session_data["unsolved_guessr"] += 1

                        break
                except asyncio.TimeoutError:
                    # When the timeout timer is finished.

                    await ctx.channel.send(
                        embed=make_embed(
                            title="Time's Up!",
                            description=f"The chamber is {guessr_answer}!",
                            color="#ededed",
                        )
                    )

                    session_data["unsolved_guessr"] += 1

                    break

                guessr_elapsed_time = time.time() - guessr_start_time

            if session_data["session_stopped"]:
                break

        user_mvp = (
            f"***{guessr_find_mvp(session_data['session_users_correct'])}*** for the most solves!"
            if session_data["session_users_correct"]
            else "No one :("
        )
        users_participated = (
            ", ".join(
                [f"`{user}`" for user in session_data["session_users_participated"]]
            )
            if len(session_data["session_users_participated"]) != 0
            else "No one participated :("
        )
        guessr_solved_count = session_data["solved_guessr"]
        guessr_unsolved_count = session_data["unsolved_guessr"]
        guessr_skipped_count = session_data["session_skipped"]

        await ctx.channel.send(
            embed=make_embed(
                "Game Result",
                f"Solved guessr(s): ***{guessr_solved_count}***\nUnsolved guessr(s): ***{guessr_unsolved_count}***\nSkipped guessr(s): ***{guessr_skipped_count}***\nParticipated user(s): {users_participated}\n\nMVP: {user_mvp}",
                BOT_COLOR,
            )
        )

        running_channels.remove(ctx.channel.id)


async def setup(bot):
    await bot.add_cog(Guessr(bot))
