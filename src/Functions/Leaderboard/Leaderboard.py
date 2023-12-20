from typing import Optional

import discord
from discord.ext import commands
from discord import app_commands

from utils.guessr_scores_req import guessr_get_all_scores, guessr_get_score
from utils.discord_utils import make_embed, make_file
from utils.calculate_seconds_since_epoch import calculate_seconds_since_epoch
from const import BOT_COLOR


class Leaderboard(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(name="lb", description="Shows the leaderboard for guessr.")
    @app_commands.describe(
        target="Target a member the current server in the leaderboard",
        target_id="Target a user in the leaderboard by their Discord's id.",
    )
    async def lb(
        self,
        ctx: commands.Context,
        target: Optional[discord.Member] = None,
        target_id: Optional[str] = None,
    ):
        await ctx.defer()

        if target != None:
            target_member_stat = await guessr_get_score(target.id)

            if not target_member_stat:
                await ctx.send(
                    f"{target.name} is not in the leaderboard!",
                    ephemeral=True,
                    delete_after=3,
                )

                return

            easy, medium, hard, veryhard = target_member_stat["scores"].values()
            started_at = calculate_seconds_since_epoch(
                target_member_stat["createdDate"]
            )
            embed = make_embed(
                description=f"Stats for {target.mention}",
                color=target.accent_color or BOT_COLOR,
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
            embed.set_author(name=target.name, icon_url=target.avatar.url)
            icon = make_file("./src/assets/icon.png", "icon.png")

            await ctx.send(embed=embed, file=icon)
        elif target_id != None:
            target_user_stat = await guessr_get_score(target_id)

            if not target_user_stat:
                await ctx.send(
                    f"{target_id} is not in the leaderboard!",
                    ephemeral=True,
                    delete_after=3,
                )

                return

            target_user = await self.bot.fetch_user(int(target_user_stat["userId"]))

            easy, medium, hard, veryhard = target_user_stat["scores"].values()
            started_at = calculate_seconds_since_epoch(
                target_member_stat["createdDate"]
            )
            embed = make_embed(
                description=target_user.mention,
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
            embed.set_author(
                name=f"Stats for {target_user.name}", icon_url=target_user.avatar.url
            )
            icon = make_file("./src/assets/icon.png", "icon.png")

            await ctx.send(embed=embed, file=icon)
        else:
            users_stat = await guessr_get_all_scores()
            sorted_users_stat = sorted(
                users_stat,
                reverse=True,
                key=lambda item: sum(item["scores"].values()),
            )
            users_stat_entry = []

            for rank, scores_datum in enumerate(sorted_users_stat, start=1):
                user = await self.bot.fetch_user(int(scores_datum["userId"]))
                easy, medium, hard, veryhard = scores_datum["scores"].values()
                users_stat_entry.append(
                    f"**{rank}.** `{user.name}` - {easy} easy, {medium} medium, {hard} hard, and {veryhard} very hard."
                )

            lb_embed = make_embed("Leaderboard", "\n".join(users_stat_entry), BOT_COLOR)
            lb_embed.set_footer(
                text=f"There are {len(users_stat)} users in the leaderboard!",
                icon_url="attachment://icon.png",
            )
            icon = make_file("./src/assets/icon.png", "icon.png")

            await ctx.send(embed=lb_embed, file=icon)


async def setup(bot):
    await bot.add_cog(Leaderboard(bot))
