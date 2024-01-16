from typing import Optional

import discord
from discord.ext import commands
from discord import app_commands

from utils.game.lb import get_all_scores, get_score
from hooks.discord.make_embed import make_embed
from hooks.discord.get_user_mention import get_user_mention
from hooks.discord.get_user import get_user
from utils.bot.make_icon import make_icon
from const import BOT_COLOR, MAX_AMOUNT


class Leaderboard(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(name="lb", description="Shows the current leaderboard.")
    @app_commands.describe(
        user="Targets a user the current server in the leaderboard",
        user_id="Targets a user in the leaderboard by their Discord's id.",
        start="The starting index (one-based index).",
        amount=f"The total amount that needs to be displayed (max: {MAX_AMOUNT}",
    )
    async def lb(
        self,
        ctx,
        user: Optional[discord.User] = None,
        user_id: Optional[str] = None,
        start: Optional[int] = 1,
        amount: Optional[int] = 10,
    ):
        await ctx.defer()

        if user:
            user_stats = await get_score(user.id)

            if user_stats == None:
                raise commands.UserNotFound(user.id)
            else:
                easy, medium, hard, veryhard = user_stats["scores"].values()
                elo = sum([easy * 3, medium * 5, hard * 10, veryhard * 15])
                started_at = user_stats["createdStamp"]

                embed = make_embed(
                    description=f"{user.mention} stats",
                    color=user.accent_color or BOT_COLOR,
                )
                embed.add_field(name="ELO", value=elo, inline=False)
                embed.add_field(name="Easy", value=easy, inline=False)
                embed.add_field(name="Medium", value=medium, inline=False)
                embed.add_field(name="Hard", value=hard, inline=False)
                embed.add_field(name="Very Hard", value=veryhard, inline=False)
                embed.add_field(
                    name="Started at", value=f"<t:{started_at}:f>", inline=False
                )
                embed.set_footer(
                    text="Keep playing to improve your stats!",
                    icon_url="attachment://icon.png",
                )
                embed.set_author(name=user.name, icon_url=user.avatar.url)

                await ctx.send(embed=embed, file=make_icon())
        elif user_id:
            user_id_stats = await get_score(user_id)

            if user_id_stats == None:
                raise commands.UserNotFound(user_id)
            else:
                target_user = await get_user(self.bot, user_id)
                target_user_mention = await get_user_mention(self.bot, user_id)
                target_user_color = (
                    target_user.accent_color if target_user != None else BOT_COLOR
                )
                target_user_name = target_user.name if target_user != None else "N/A"
                target_user_avatar = (
                    target_user.avatar.url
                    if target_user != None
                    else "attachment://icon.png"
                )

                easy, medium, hard, veryhard = user_id_stats["scores"].values()
                elo = sum([easy * 3, medium * 5, hard * 10, veryhard * 15])
                started_at = user_id_stats["createdStamp"]

                embed = make_embed(
                    description=f"{target_user_mention} stats",
                    color=target_user_color,
                )
                embed.add_field(name="ELO", value=elo, inline=False)
                embed.add_field(name="Easy", value=easy, inline=False)
                embed.add_field(name="Medium", value=medium, inline=False)
                embed.add_field(name="Hard", value=hard, inline=False)
                embed.add_field(name="Very Hard", value=veryhard, inline=False)
                embed.add_field(
                    name="Started at", value=f"<t:{started_at}:f>", inline=False
                )
                embed.set_footer(
                    text="Keep playing to improve your stats!",
                    icon_url="attachment://icon.png",
                )
                embed.set_author(name=target_user_name, icon_url=target_user_avatar)

                await ctx.send(embed=embed, file=make_icon())
        else:
            users_stats = await get_all_scores()
            users_stats_length = len(users_stats)

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

            if users_stats_length != 0:
                if start > users_stats_length:
                    await ctx.send(
                        f"Start value cannot exceed {users_stats_length}!",
                        ephemeral=True,
                    )

                    return
                elif start <= 0:
                    await ctx.send(
                        "Starting index cannot be less than or equal to 0!",
                        ephemeral=True,
                    )

                    return

            sorted_users_stat = sorted(
                users_stats,
                reverse=True,
                key=lambda user_stat: sum(
                    [
                        user_stat["scores"]["Easy"] * 3,
                        user_stat["scores"]["Medium"] * 5,
                        user_stat["scores"]["Hard"] * 10,
                        user_stat["scores"]["Very Hard"] * 15,
                    ]
                ),
            )
            users_stat_entry = []
            adjusted_amount = (
                (start + amount) - 1
                if not start + amount > users_stats_length
                else users_stats_length
            )
            adjusted_end_index = (
                adjusted_amount if start != users_stats_length else adjusted_amount + 1
            )

            for rank, user_stats in enumerate(sorted_users_stat, start=1):
                user_mention = await get_user_mention(self.bot, user_stats["userId"])
                easy, medium, hard, veryhard = user_stats["scores"].values()
                elo = sum([easy * 3, medium * 5, hard * 10, veryhard * 15])

                entry_message = f"{rank}. {user_mention} at **{elo}** ELO"
                users_stat_entry.append(entry_message)

            data_entry = users_stat_entry[start - 1 : adjusted_end_index]
            data_entry_length = len(data_entry)
            embed_description = "\n".join(data_entry) or "Empty :("

            lb_embed = make_embed(
                "Leaderboard",
                embed_description,
                BOT_COLOR,
            )
            lb_embed.set_footer(
                text=f"Showing {data_entry_length} out of {users_stats_length} total.",
                icon_url="attachment://icon.png",
            )

            await ctx.send(embed=lb_embed, file=make_icon())


async def setup(bot):
    await bot.add_cog(Leaderboard(bot))
