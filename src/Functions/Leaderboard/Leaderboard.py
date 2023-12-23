from typing import Optional

import discord
from discord.ext import commands
from discord import app_commands

from utils.guessr.lb import get_all_scores, get_score
from hooks.discord.use_discord import make_embed
from const import BOT_COLOR, BOT_MAKE_ICON


class Leaderboard(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(name="lb", description="Shows the current leaderboard.")
    @app_commands.describe(
        user="Targets a user the current server in the leaderboard",
        user_id="Targets a user in the leaderboard by their Discord's id.",
    )
    async def lb(
        self,
        ctx: commands.Context,
        user: Optional[discord.User] = None,
        user_id: Optional[str] = None,
    ):
        await ctx.defer()

        if user != None:
            target_member_stat = await get_score(user.id)

            if not target_member_stat:
                await ctx.send(
                    f"{user.mention} is not in the leaderboard!",
                    ephemeral=True,
                )

                return

            easy, medium, hard, veryhard = target_member_stat["scores"].values()
            started_at = target_member_stat["createdStamp"]
            embed = make_embed(
                description=f"Stats for {user.mention}",
                color=user.accent_color or BOT_COLOR,
            )
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

            await ctx.send(embed=embed, file=BOT_MAKE_ICON())
        elif user_id != None:
            target_user_stat = await get_score(user_id)

            if not target_user_stat:
                await ctx.send(
                    f"{user_id} is not in the leaderboard!",
                    ephemeral=True,
                )

                return

            target_user = await self.bot.fetch_user(int(user_id))
            easy, medium, hard, veryhard = target_user_stat["scores"].values()
            started_at = target_user_stat["createdStamp"]
            embed = make_embed(
                description=f"Stats for {target_user.mention}",
                color=target_user.accent_color or BOT_COLOR,
            )
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
            embed.set_author(name=target_user.name, icon_url=target_user.avatar.url)

            await ctx.send(embed=embed, file=BOT_MAKE_ICON())
        else:
            users_stat = await get_all_scores()
            sorted_users_stat = sorted(
                users_stat,
                reverse=True,
                key=lambda item: sum(item["scores"].values()),
            )
            users_stat_entry = []

            for rank, user_stat in enumerate(sorted_users_stat, start=1):
                user_mention = (
                    await self.bot.fetch_user(int(user_stat["userId"]))
                ).mention
                easy, medium, hard, veryhard = user_stat["scores"].values()
                users_stat_entry.append(
                    f"{rank}. {user_mention} - **{easy}** easy, **{medium}** medium, **{hard}** hard, and **{veryhard}** very hard."
                )

            lb_embed = make_embed("Leaderboard", "\n".join(users_stat_entry), BOT_COLOR)
            lb_embed.set_footer(
                text=f"There are {len(users_stat)} users in the leaderboard!",
                icon_url="attachment://icon.png",
            )

            await ctx.send(embed=lb_embed, file=BOT_MAKE_ICON())


async def setup(bot):
    await bot.add_cog(Leaderboard(bot))
