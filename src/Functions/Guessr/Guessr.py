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
from hooks.discord.use_discord import make_embed, get_user_mention
from utils.bot.utils import bot_make_icon
from utils.guessr.history import add_history
from const import BOT_COLOR, CHAMBERS


class Guessr(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.channels_running = []

    @commands.hybrid_command(name="guess", description="Starts a PortalGuessr game.")
    @app_commands.describe(
        difficulty="The desired difficulty (leave blank to keep it random).",
        rounds="The amount of rounds in a session (max: 50).",
    )
    async def guess(
        self,
        ctx: commands.Context,
        difficulty: Optional[Literal["Easy", "Medium", "Hard", "Very Hard"]] = "Random",
        rounds: Optional[int] = 10,
    ):
        try:

            def response_is_valid(message):
                # Check the validity of the respondent's message.
                return (
                    message.guild.id == ctx.guild.id
                    and message.channel.id == ctx.channel.id
                    and message.content.lower() in CHAMBERS + ["skip", "stop"]
                )

            if ctx.channel.id in self.channels_running:
                await ctx.send(
                    f"Only one instance of a game can be running at the same channel at the same time!",
                    ephemeral=True,
                )

                return

            if rounds <= 0:
                await ctx.send(
                    "The amount of rounds must be higher than 0!",
                    ephemeral=True,
                )

                return
            elif rounds > 25:
                await ctx.send(
                    "You're exceeding the limit! I'm not sure if you can finish that many...",
                    ephemeral=True,
                )

                return

            await ctx.defer()

            try:
                chambers = (
                    await get_chambers(rounds, difficulty)
                    if difficulty != "Random"
                    else await get_random_chambers(rounds)
                )
            except Exception as e:
                raise commands.CommandError(e)

            self.channels_running.append(ctx.channel.id)
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
                    file=bot_make_icon(),
                ) if round == 1 else await ctx.channel.send(
                    embed=embed,
                    file=bot_make_icon(),
                )

                while True:
                    try:
                        response = await self.bot.wait_for(
                            "message",
                            check=response_is_valid,
                            timeout=timeout - elapsed_time,
                        )

                        if response.content.lower() in ["skip", "stop"]:
                            if response.author.id != ctx.author.id:
                                # Responder must be the prompter.
                                await response.reply(
                                    embed=make_embed(
                                        title="You're not allowed to use this command!",
                                        description="Only the user prompted this guessr is eligible to use this command.",
                                        color=BOT_COLOR,
                                    ),
                                    delete_after=3,
                                    mention_author=False,
                                )

                                continue

                            if response.content.lower() == "skip":
                                game_log["skipped"] += 1

                                await response.reply(
                                    embed=make_embed(
                                        title="Guessr Skipped!", color=BOT_COLOR
                                    ),
                                    mention_author=False,
                                )

                                break
                            elif response.content.lower() == "stop":
                                if round == 1:
                                    await response.reply(
                                        embed=make_embed(
                                            title="Finish the first round first to stop the game!",
                                            color=BOT_COLOR,
                                        ),
                                        mention_author=False,
                                    )

                                    continue

                                game_stopped = True

                                await response.reply(
                                    embed=make_embed(
                                        title="Guessr Stopped!", color=BOT_COLOR
                                    ),
                                    mention_author=False,
                                )

                                break

                        if (
                            # If the responder has responded once.
                            response.author.id
                            in data["user_ids_have_answered"]
                        ):
                            await response.reply(
                                embed=make_embed(
                                    title="You have answered!",
                                    color=BOT_COLOR,
                                ),
                                delete_after=3,
                                mention_author=False,
                            )

                            continue

                        if (
                            str(response.author.id)
                            not in game_log["user_ids_participated"]
                        ):
                            game_log["user_ids_participated"].append(
                                str(response.author.id)
                            )

                        data["user_ids_have_answered"].append(response.author.id)
                        data["answer_count"] += 1

                        if response.content.lower() == answer:
                            game_log["solved"] += 1
                            game_log["user_ids_correct"].append(str(response.author.id))

                            await response.add_reaction("✅")
                            await update_user_stats(
                                response.author.id, guessr_difficulty
                            )

                            break
                        else:
                            await response.add_reaction("❌")

                        if data["answer_count"] >= data["answer_count_max"]:
                            # After 5 respondents.
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
            game_id = None
            user_mvp = find_mvp(game_log["user_ids_correct"]) or ""

            try:
                # Saving game result to the database.
                game_id = await add_history(
                    total_chambers,
                    solved_count,
                    unsolved_count,
                    skipped_count,
                    user_mvp,
                    game_log["user_ids_participated"],
                    chambers_log,
                    str(ctx.author.id),
                    difficulty,
                )
            except Exception as e:
                raise commands.CommandError(e)

            users_participated = []

            for user_id in game_log["user_ids_participated"]:
                users_participated.append(await get_user_mention(user_id))

            user_mvp_text = (
                f"{await get_user_mention(user_id)} for the most solves!"
                if game_log["user_ids_correct"]
                else "No one :("
            )
            users_participated_text = (
                ", ".join(users_participated)
                if len(game_log["user_ids_participated"]) != 0
                else "No one participated :("
            )
            footer_text = (
                f"Game ID: {game_id}"
                if game_id != None
                else "This game is not recorded!"
            )

            embed_stats = make_embed(
                "Game result",
                f"Solved guessr(s): ***{solved_count}***\nUnsolved guessr(s): ***{unsolved_count}***\nSkipped guessr(s): ***{skipped_count}***\nParticipated user(s): {users_participated_text}\n\nMVP: {user_mvp_text}",
                BOT_COLOR,
            )
            embed_stats.set_footer(
                text=footer_text,
                icon_url="attachment://icon.png",
            )

            await ctx.channel.send(embed=embed_stats, file=bot_make_icon())
        except Exception as e:
            self.channels_running.remove(ctx.channel.id)

            raise commands.CommandError(e)
        else:
            self.channels_running.remove(ctx.channel.id)


async def setup(bot):
    await bot.add_cog(Guessr(bot))
