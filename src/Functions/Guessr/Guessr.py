# TODO: Refactor the code cuz it's garbo af.

import asyncio
import time
from typing import Literal, Optional

import discord
from discord import app_commands
from discord.ext import commands

from utils.guessr.lb_utils import update_user_stats
from utils.guessr.chambers import (
    get_chambers,
    get_random_chambers,
)
from utils.guessr.utils import (
    find_mvp,
    get_color,
    get_timeout,
)
from hooks.discord.use_discord import make_embed, make_file
from utils.guessr.history import add_history
from const import BOT_COLOR, CHAMBERS, XNONXTE_USER_ID


class Guessr(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.channels_running = []

    @commands.hybrid_command(name="guess", description="Starts a PortalGuessr game.")
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
        prompter_id = ctx.author.id
        channel_id = ctx.channel.id

        def res_is_valid(message: discord.Message):
            # Check the validity of the responder's message.
            return (
                message.guild.id == ctx.guild.id
                and message.channel.id == channel_id
                and message.content.lower() in CHAMBERS + ["skip", "stop"]
            )

        if rounds <= 0:
            await ctx.send(
                "The amount of rounds must be higher than 0!",
                ephemeral=True,
            )
            return
        if channel_id in self.channels_running:
            await ctx.send(
                f"A game is already running in {ctx.channel.mention}. Please wait for it to finish or start another instance in a different channel!",
                ephemeral=True,
            )
            return

        await ctx.defer()  # Defer the command.

        try:
            chambers = (
                await get_chambers(rounds, difficulty)
                if difficulty != "Random"
                else await get_random_chambers(rounds)
            )
        except Exception as e:
            await ctx.send(
                embed=make_embed(
                    "Uh Oh...",
                    f"Failed while fetching data from the server, please contact {user_xnonxte.mention}! Cause: {e}",
                    BOT_COLOR,
                )
            )

            return

        self.channels_running.append(channel_id)
        game_log = {
            # Data per session.
            "solved": 0,
            "timeout": 0,
            "skipped": 0,
            "user_ids_participated": [],
            "user_ids_correct": [],
        }
        chambers_log = [chamber["fileId"] for chamber in chambers]
        game_stopped = False

        for round, chamber in enumerate(chambers, start=1):
            image_url = chamber["url"]
            answer = chamber["answer"]
            guessr_difficulty = chamber["difficulty"]

            start_time = time.time()
            elapsed_time = 0
            timeout = get_timeout(guessr_difficulty)

            data = {
                # Data per guessr.
                "user_ids_have_answered": [],
                "answer_count": 0,
                "answer_count_max": 5,
            }

            embed = make_embed(
                title="Guess the chamber!",
                color=get_color(guessr_difficulty),
            )
            embed.set_image(url=image_url)
            embed.set_footer(
                text=f"Round {round} of {rounds} - skip | stop",
                icon_url="attachment://icon.png",
            )

            await ctx.send(
                embed=embed,
                file=make_file("./src/assets/icon.png", "icon.png"),
            ) if round == 1 else await ctx.channel.send(
                embed=embed,
                file=make_file("./src/assets/icon.png", "icon.png"),
            )

            while True:
                try:
                    res = await self.bot.wait_for(
                        "message",
                        check=res_is_valid,
                        timeout=timeout - elapsed_time,
                    )

                    res_lower = res.content.lower()
                    res_id = res.author.id

                    if res_lower in ["skip", "stop"]:
                        if res_id != prompter_id:
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
                            game_log["skipped"] += 1

                            await res.reply(
                                embed=make_embed(
                                    title="Guessr Skipped!", color=BOT_COLOR
                                ),
                                mention_author=False,
                            )

                            break
                        elif res_lower == "stop":
                            if round == 1:
                                await res.reply(
                                    embed=make_embed(
                                        title="Finish the first round first to stop the game!",
                                        color=BOT_COLOR,
                                    ),
                                    mention_author=False,
                                )

                                continue

                            game_stopped = True
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
                        in data["user_ids_have_answered"]
                    ):
                        await res.reply(
                            embed=make_embed(
                                title="You have answered!",
                                color=BOT_COLOR,
                            ),
                            delete_after=3,
                            mention_author=False,
                        )

                        continue

                    if str(res_id) not in game_log["user_ids_participated"]:
                        game_log["user_ids_participated"].append(str(res_id))

                    data["user_ids_have_answered"].append(res_id)
                    data["answer_count"] += 1

                    if res_lower == answer:
                        game_log["solved"] += 1
                        game_log["user_ids_correct"].append(str(res_id))
                        await update_user_stats(res_id, guessr_difficulty)
                        await res.add_reaction("✅")

                        break
                    else:
                        await res.add_reaction("❌")

                    if data["answer_count"] >= data["answer_count_max"]:
                        # After 5 respondent.
                        await ctx.channel.send(
                            embed=make_embed(
                                title="Game Finished!",
                                description=f"5 users have attempted at guessing this chamber, but no one got it right!\nThe chamber is {answer}!",
                                color=BOT_COLOR,
                            )
                        )
                        game_log["timeout"] += 1

                        break
                except asyncio.TimeoutError:
                    # When the timeout timer is finished.
                    await ctx.channel.send(
                        embed=make_embed(
                            title="Time's Up!",
                            description=f"The chamber is {answer}!",
                            color="#ededed",
                        )
                    )
                    game_log["timeout"] += 1

                    break

                elapsed_time = time.time() - start_time

            if game_stopped == True:
                break

        total_chambers = len(chambers)
        solved_count = game_log["solved"]
        unsolved_count = game_log["timeout"]
        skipped_count = game_log["skipped"]
        history_id = None
        user_mvp = find_mvp(game_log["user_ids_correct"]) or ""

        try:
            # Saving game result to the database.
            history_id = await add_history(
                total_chambers,
                solved_count,
                unsolved_count,
                skipped_count,
                user_mvp,
                game_log["user_ids_participated"],
                chambers_log,
                str(prompter_id),
                difficulty,
            )
        except Exception as e:
            user_xnonxte = await self.bot.fetch_user(XNONXTE_USER_ID)

            await ctx.send(
                embed=make_embed(
                    "Error Occurred!",
                    f"Failed while uploading game result to the server, please contact {user_xnonxte.mention}! Cause: {e}",
                    BOT_COLOR,
                )
            )

        try:
            user_mvp_name = (await self.bot.fetch_user(user_mvp)).mention
        except discord.NotFound:
            pass

        users_participated = []
        for user_id in game_log["user_ids_participated"]:
            users_participated.append((await self.bot.fetch_user(int(user_id))).mention)

        user_mvp_text = (
            f"{user_mvp_name} for the most solves!"
            if game_log["user_ids_correct"]
            else "No one :("
        )
        users_participated_text = (
            ", ".join(users_participated)
            if len(game_log["user_ids_participated"]) != 0
            else "No one participated :("
        )

        embed_stats = make_embed(
            "Game Result",
            f"Solved guessr(s): ***{solved_count}***\nUnsolved guessr(s): ***{unsolved_count}***\nSkipped guessr(s): ***{skipped_count}***\nParticipated user(s): {users_participated_text}\n\nMVP: {user_mvp_text}",
            BOT_COLOR,
        )
        embed_stats.set_footer(
            text=f"Game has been recorded! Try /history <{history_id}>"
            if history_id != None
            else "Unfortunately this game is not recorded, please try again later!",
            icon_url="attachment://icon.png",
        )

        await ctx.channel.send(
            embed=embed_stats, file=make_file("./src/assets/icon.png", "icon.png")
        )

        self.channels_running.remove(channel_id)


async def setup(bot):
    await bot.add_cog(Guessr(bot))
