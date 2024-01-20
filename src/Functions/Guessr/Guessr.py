import asyncio
import time
from typing import Literal, Optional

from discord import app_commands
from discord.ext import commands

from utils.game.lb import update_user_statistic
from utils.game.chambers import (
    get_chambers,
    get_random_chambers,
)
from utils.game.guessr import (
    find_mvp,
    get_color,
    get_timeout,
)
from hooks.discord.make_embed import make_embed
from hooks.discord.get_user_mention import get_user_mention
from utils.bot.make_icon import make_icon
from utils.game.history import add_history
from const import (
    BOT_COLOR,
    BOT_COLOR_WHITE,
    CHAMBERS,
    MAX_ROUNDS,
    P1SR_GUILD_ID,
    P1SR_SPAM_CHANNEL_ID,
)


class Guessr(commands.Cog):
    """Cog for guessr related command.

    Args:
        commands (commands.Bot): The bot's instance.

    Raises:
        commands.CommandError: In the case of error, this cog will raise commands.CommandError exception.
    """

    active_game_channels = set()

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(name="guess", description="Starts a PortalGuessr game.")
    @commands.guild_only()
    @app_commands.describe(
        difficulty="The desired difficulty (leave blank to keep it random).",
        rounds=f"The amount of rounds in a session (max: {MAX_ROUNDS}).",
    )
    async def guess(
        self,
        ctx,
        difficulty: Optional[Literal["Easy", "Medium", "Hard", "Very Hard"]] = "Random",
        rounds: Optional[int] = 10,
    ):
        try:
            if ctx.channel.id in self.active_game_channels:
                await ctx.send(
                    "Only one game can be running at the same channel at the same time!",
                    ephemeral=True,
                )

                return

            if ctx.guild.id == P1SR_GUILD_ID:
                if ctx.channel.id != P1SR_SPAM_CHANNEL_ID:
                    await ctx.send(
                        f"This command is only permitted to be invoked in {ctx.guild.get_channel(P1SR_SPAM_CHANNEL_ID).mention} while in P1SR!",
                        ephemeral=True,
                    )

                    return

            if rounds <= 0:
                await ctx.send(
                    "Rounds must be higher than 0!",
                    ephemeral=True,
                )

                return
            elif rounds > MAX_ROUNDS:
                await ctx.send(
                    "You're exceeding rounds limit!",
                    ephemeral=True,
                )

                return

            await ctx.defer()
            chambers = (
                await get_chambers(rounds, difficulty)
                if difficulty != "Random"
                else await get_random_chambers(rounds)
            )

            game_log = {
                # Data per game.
                "solved": 0,
                "timeout": 0,
                "skipped": 0,
                "user_ids_participated": [],
                "user_ids_correct": [],
                "ignored_continuous_guessrs_count": 0,
            }
            chambers_log = [chamber["fileId"] for chamber in chambers]
            game_stopped = False

            self.active_game_channels.add(ctx.channel.id)

            for round_count, chamber in enumerate(chambers, start=1):
                image_url, answer, guessr_difficulty = (
                    chamber["url"],
                    chamber["answer"],
                    chamber["difficulty"],
                )

                start_time = time.time()
                elapsed_time = 0
                timeout = get_timeout(guessr_difficulty)

                guessr_tmp_data = {
                    # Data per guessr.
                    "user_ids_have_answered": [],
                    "answer_count": 0,
                    "answer_count_max": 7,
                }

                embed = make_embed(
                    title="Guess the chamber!",
                    color=get_color(guessr_difficulty),
                )
                embed.set_image(url=image_url)
                embed.set_footer(
                    text=f"Round {round_count} of {rounds} - skip | stop",
                    icon_url="attachment://icon.png",
                )

                if round_count == 1:
                    await ctx.send(embed=embed, file=make_icon())
                else:
                    await ctx.channel.send(
                        embed=embed,
                        file=make_icon(),
                    )

                while True:
                    # Forever loop, but not quite a forever loop.
                    try:
                        response = await self.bot.wait_for(
                            "message",
                            check=lambda m: m.guild.id == ctx.guild.id
                            and m.channel.id == ctx.channel.id
                            and m.content.lower() in CHAMBERS + ["skip", "stop"],
                            timeout=timeout - elapsed_time,
                        )

                        if response.content.lower() in ["skip", "stop"]:
                            if (
                                response.author.id == ctx.author.id
                                or response.author.guild_permissions.moderate_members
                            ):
                                # Responder must be the prompter.
                                if response.content.lower() == "skip":
                                    if guessr_tmp_data["answer_count"] == 0:
                                        await response.reply(
                                            embed=make_embed(
                                                title="Have one answer first!",
                                                color=BOT_COLOR,
                                            ),
                                            mention_author=False,
                                            delete_after=5,
                                        )

                                        continue

                                    game_log["skipped"] += 1

                                    await response.reply(
                                        embed=make_embed(
                                            title="Guessr Skipped!", color=BOT_COLOR
                                        ),
                                        mention_author=False,
                                    )

                                    break
                                elif response.content.lower() == "stop":
                                    if round_count == 1:
                                        await response.reply(
                                            embed=make_embed(
                                                title="Finish the first round first!",
                                                color=BOT_COLOR,
                                            ),
                                            mention_author=False,
                                            delete_after=5,
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
                            else:
                                await response.reply(
                                    embed=make_embed(
                                        title="You're not allowed to use this command!",
                                        description="Only the user prompted this guessr (or a moderator) is eligible to use this command.",
                                        color=BOT_COLOR,
                                    ),
                                    delete_after=3,
                                    mention_author=False,
                                )

                                continue

                        if (
                            # If the responder has responded once.
                            response.author.id
                            in guessr_tmp_data["user_ids_have_answered"]
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

                        guessr_tmp_data["user_ids_have_answered"].append(
                            response.author.id
                        )
                        guessr_tmp_data["answer_count"] += 1

                        if response.content.lower() == answer:
                            game_log["solved"] += 1
                            game_log["user_ids_correct"].append(str(response.author.id))

                            await response.add_reaction("✅")
                            await update_user_statistic(
                                response.author.id, guessr_difficulty
                            )

                            break
                        else:
                            await response.add_reaction("❌")

                        if (
                            guessr_tmp_data["answer_count"]
                            >= guessr_tmp_data["answer_count_max"]
                        ):
                            await ctx.channel.send(
                                embed=make_embed(
                                    title="Guessr Finished!",
                                    description=f"7 people have tried to answer this guessr, but no one got it right! The chamber is {answer}!",
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
                                color=BOT_COLOR_WHITE,
                            )
                        )
                        game_log["timeout"] += 1

                        break

                    elapsed_time = time.time() - start_time

                if guessr_tmp_data["answer_count"] == 0:
                    game_log["ignored_continuous_guessrs_count"] += 1
                else:
                    # Reset the count.
                    game_log["ignored_continuous_guessrs_count"] = 0

                if game_log["ignored_continuous_guessrs_count"] == 2:
                    await ctx.send(
                        embed=make_embed(
                            "Abandoned game detected! Stopping current game...",
                            color=BOT_COLOR,
                        )
                    )

                    break

                if game_stopped == True:
                    break

            total_chambers = len(chambers)
            solved_count, unsolved_count, skipped_count = (
                game_log["solved"],
                game_log["timeout"],
                game_log["skipped"],
            )
            user_mvp = find_mvp(game_log["user_ids_correct"]) or ""
            user_mvp_mention = await get_user_mention(self.bot, user_mvp)
            history_id = await add_history(
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
            users_participated = [
                await get_user_mention(self.bot, user_id)
                for user_id in game_log["user_ids_participated"]
            ]
            user_mvp_text = (
                f"{user_mvp_mention} for the most solves!"
                if game_log["user_ids_correct"]
                else "No one :("
            )
            users_participated_text = (
                ", ".join(users_participated)
                if game_log["user_ids_participated"]
                else "No one participated :("
            )
            footer_text = f"History ID: {history_id}"

            embed_stats = make_embed(
                "Game result",
                f"Solved guessr(s): ***{solved_count}***\nUnsolved guessr(s): ***{unsolved_count}***\nSkipped guessr(s): ***{skipped_count}***\nParticipated user(s): {users_participated_text}\n\nMVP: {user_mvp_text}",
                BOT_COLOR,
            )
            embed_stats.set_footer(
                text=footer_text,
                icon_url="attachment://icon.png",
            )

            await ctx.channel.send(embed=embed_stats, file=make_icon())
        except Exception as e:
            self.active_game_channels.discard(ctx.channel.id)

            await ctx.send(
                embed=make_embed("Error detected! Game is stopped!", color=BOT_COLOR)
            )

            raise commands.CommandError(e)
        else:
            self.active_game_channels.discard(ctx.channel.id)


async def setup(bot):
    await bot.add_cog(Guessr(bot))
