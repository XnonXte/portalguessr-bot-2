import discord
from discord.ext import commands
from discord import app_commands

from hooks.discord.use_discord import make_embed
from utils.guessr.lb import add_score, remove_score
from const import (
    OWNER_USER_ID,
    BOT_COLOR,
    BOT_MAKE_ICON,
    DEFAULT_FOOTER_TEXT,
)


class MyCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(
        name="lb_add",
        description="Adds a new stats to the leaderboard (owner only command).",
    )
    @app_commands.describe(
        user_id="A valid user ID on Discord.",
        easy_count="The number of easy guessrs.",
        medium_count="The number of medium guessrs.",
        hard_count="The number of hard guessrs.",
        very_hard_count="The number of very hard guessrs.",
    )
    async def lb_add(
        self,
        ctx,
        user_id: str,
        easy_count: int,
        medium_count: int,
        hard_count: int,
        very_hard_count: int,
    ):
        if ctx.author.id != OWNER_USER_ID:
            raise commands.NotOwner(
                f"Author's ID ({ctx.author.id}) is not equal to {OWNER_USER_ID}"
            )

        await ctx.defer()

        data = {
            "scores": {
                "Easy": easy_count,
                "Medium": medium_count,
                "Hard": hard_count,
                "Very Hard": very_hard_count,
            }
        }

        try:
            result = await add_score(user_id, data)

            user_mention = (await self.bot.fetch_user(int(user_id))).mention
            embed = make_embed(
                "Success!", f"Stats for {user_mention} has been created!", BOT_COLOR
            )
            embed.set_footer(
                text=f"MongoDB ID: {result['_id']}", icon_url="attachment://icon.png"
            )

            await ctx.send(embed=embed, file=BOT_MAKE_ICON())
        except Exception as e:
            print(e)
            await ctx.send(
                f"Failed to add `{user_id}` stats to the leaderboard!",
                ephemeral=True,
            )

    @commands.hybrid_command(
        help="lb_rm",
        description="Removes an existing stats from the leaderboard (owner only command).",
    )
    @app_commands.describe(user_id="The target's user ID on Discord.")
    async def lb_rm(self, ctx, user_id: str):
        if ctx.author.id != OWNER_USER_ID:
            raise commands.NotOwner(
                f"Author's ID ({ctx.author.id}) is not equal to {OWNER_USER_ID}"
            )

        await ctx.defer()

        try:
            result = await remove_score(int(user_id))
            if result["deletedCount"] == 0:
                await ctx.send(
                    f"Stats for user with ID: {user_id} does not exist!", ephemeral=True
                )

                return

            user_mention = (await self.bot.fetch_user(int(user_id))).mention

            embed = make_embed(
                "Success!",
                f"{user_mention} stats in the leaderboard has been removed!!",
                BOT_COLOR,
            )
            embed.set_footer(text=DEFAULT_FOOTER_TEXT, icon_url="attachment://icon.png")

            await ctx.send(embed=embed, file=BOT_MAKE_ICON())
        except Exception as e:
            print(e)
            await ctx.send(
                f"Failed to remove `{user_id}` stats from the leaderboard!",
                ephemeral=True,
            )


async def setup(bot):
    await bot.add_cog(MyCog(bot))
