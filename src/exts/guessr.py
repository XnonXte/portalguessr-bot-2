import asyncio
import time
from typing import Literal, Optional

import discord
from discord import app_commands
from discord.ext import commands

from utils.get_guessr import GetGuessr
from utils.get_guessr_timeout import get_guessr_timeout
from utils.get_guessr_color import get_guessr_color
from misc.const import BOT_COLOR, GUESSR_CHAMBERS
from utils.find_mvp import find_mvp

running_channels = []


class Guessr(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(name="guess", description="Starts the game.")
    @app_commands.describe(
        difficulty="Your desired difficulty.",
        rounds="The amount of rounds.",
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
                "The amount of rounds must be higher than 0!", ephemeral=True
            )
            return
        if ctx.channel.id in running_channels:
            await ctx.send(
                f"A game is already running in #{ctx.channel.id}, please wait for it to finish or start another one in a different channel!"
            )

        session_data = {
            # Data per session.
            "correct_count": 0,
            "incorrect_count": 0,
            "session_skipped": 0,
            "session_users_participated": [],
            "session_users_correct": [],
            "session_stopped": False,
        }

        try:
            guessr_chambers = GetGuessr.get_chambers(rounds, difficulty)
        except Exception as e:
            print(e)

        for guessr_chamber in guessr_chambers:
            guessr_image_url = guessr_chamber["url"]
            guessr_answer = guessr_chamber["answer"]
            guessr_difficulty = guessr_chamber["difficulty"]

            guessr_start_time = time.time()
            guessr_elapsed_time = 0
            guessr_timeout = get_guessr_timeout(guessr_difficulty)

            guessr_data = {
                # Data per guessr.
                "guessr_user_id_have_answered": [],
                "guessr_answer_count": 0,
                "guessr_answer_count_max": 5,
            }

            guessr_embed = discord.Embed(
                title="Guess this chamber!",
                color=get_guessr_color(guessr_difficulty),
            )
            guessr_embed.set_image(url=guessr_image_url)

            if round == 0:
                await ctx.send(
                    embed=guessr_embed,
                )
            else:
                await ctx.channel.send(
                    embed=guessr_embed,
                )

            while True:
                try:
                    response: discord.Message = await self.bot.wait_for(
                        "message",
                        check=is_valid,
                        timeout=guessr_timeout - guessr_elapsed_time,
                    )

                    if response.content == "skip" or response.content == "stop":
                        if response.author.id != ctx.author.id:
                            # Responder must be the prompter.
                            await response.reply(
                                "You're not the one prompted this command!",
                                delete_after=3,
                                mention_author=False,
                            )

                            continue

                        if response.content == "skip":
                            session_data["session_skipped"] += 1

                            guessr_skipped_embed = discord.Embed(
                                color=BOT_COLOR, title="Guessr Skipped!"
                            )

                            await ctx.channel.send(embed=guessr_skipped_embed)

                            break
                        elif response.content == "stop":
                            session_data["session_stopped"] = True

                            guessr_stopped_embed = discord.Embed(
                                color=BOT_COLOR, title="Guessr Stopped!"
                            )

                            await ctx.channel.send(embed=guessr_stopped_embed)

                            break
                    if (
                        # If the responder has responded once.
                        response.author.id
                        in guessr_data["guessr_user_id_have_answered"]
                    ):
                        await response.reply(
                            "You have answered this guessr!",
                            delete_after=3,
                            mention_author=False,
                        )

                        continue

                    username = ctx.guild.get_member(response.author.id)

                    if username not in session_data["session_users_participated"]:
                        session_data["session_user_participated"].append(username)

                    guessr_data["guessr_user_id_have_answered"].append(
                        str(response.author.id)
                    )
                    guessr_data["guessr_answer_count"] += 1

                    if response.content.lower() == guessr_answer:
                        session_data["correct_count"] += 1
                        session_data["session_users_correct"].append(username)
                    else:
                        session_data["incorrect_count"] += 1

                    if (
                        guessr_data["guessr_answer_count"]
                        >= guessr_data["guessr_answer_count_max"]
                    ):
                        # After 5 respondent.
                        guessr_finished_embed = discord.Embed(
                            color=discord.Color.from_str("#efefef"),
                            title="Guessr Finished",
                            description=f"5 users have attempted at guessing this chamber, but no one got it right!\nThe chamber is {guessr_answer}!",
                        )

                        await ctx.channel.send(embed=guessr_finished_embed)

                        break
                except asyncio.TimeoutError:
                    # When the timeout timer is finished.
                    guessr_timeout_embed = discord.Embed(
                        color=discord.Color.from_str("#efefef"),
                        title="Time's Up!",
                        description=f"The chamber is {guessr_answer}!",
                    )

                    await ctx.channel.send(embed=guessr_timeout_embed)

                    break

                guessr_elapsed_time = time.time() - guessr_start_time

            if session_data["session_stopped"]:
                break

        session_result_embed = discord.Embed(
            title="Game Result",
            color=BOT_COLOR,
            description=f"correct guessr(s): ***{session_data['correct_count']}***\nIncorrect guessr(s): ***{session_data['incorrect_count']}***\nUser(s) participated: {', '.join(session_data['session_users_participated'])}\nMVP: {find_mvp(session_data['session_users_correct'])}",
        )

        await ctx.channel.send(embed=session_result_embed)


async def setup(bot):
    await bot.add_cog(Guessr(bot))
