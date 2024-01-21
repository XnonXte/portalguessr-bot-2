from typing import Optional
from datetime import datetime

from discord.ext import commands
from discord import app_commands

from hooks.discord.make_embed import make_embed
from hooks.discord.get_user_mention import get_user_mention
from hooks.discord.get_user import get_user
from hooks.python.use_enumerate import use_enumerate
from utils.game.history import read_history, read_one_history
from utils.bot.make_icon import make_icon
from const import BOT_COLOR, MAX_LIMIT, DEFAULT_LIMIT


class History(commands.Cog):
    """Cog for history related command.

    Args:
        commands (commands.Bot): The bot's instance.
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(
        name="history", description="Checks recent guessrs history."
    )
    @app_commands.describe(
        history_id="Targets a specific game from history with its ID.",
        skip="Skip to the given number (defaults to 1).",
        limit=f"The total amount that needs to be displayed (defaults to {DEFAULT_LIMIT}, {MAX_LIMIT} maximum)",
    )
    async def history(
        self,
        ctx,
        history_id: Optional[str],
        skip: Optional[int] = 1,
        limit: Optional[int] = DEFAULT_LIMIT,
    ):
        await ctx.defer()

        if history_id:
            game = await read_one_history(history_id)

            if game == None:
                raise commands.BadArgument(f"{history_id} is not a valid history ID!")
            else:
                formatted_time = datetime.fromtimestamp(game["createdStamp"]).strftime(
                    "%B %d, %Y %I:%M %p"
                )

                mvp = await get_user_mention(self.bot, game["mvp"])
                prompter = await get_user(self.bot, game["prompterUserId"])
                prompter_name = prompter.name if prompter != None else "N/A"
                prompter_avatar = (
                    prompter.avatar.url if prompter != None else "attachment://icon.png"
                )

                embed = make_embed(
                    description=f"Game prompted by: {prompter.mention}",
                    color=BOT_COLOR,
                )
                embed.add_field(name="Solved", value=game["solved"])
                embed.add_field(name="Timed out", value=game["timeout"])
                embed.add_field(name="Skipped", value=game["skipped"])
                embed.add_field(name="Difficulty", value=game["difficulty"])
                embed.add_field(name="MVP", value=mvp)
                embed.add_field(name="Participated", value=len(game["participators"]))
                embed.set_author(name=prompter_name, icon_url=prompter_avatar)
                embed.set_footer(
                    text=f"ID: {game['historyId']} | Finished at • {formatted_time}",
                    icon_url="attachment://icon.png",
                )

                await ctx.send(embed=embed, file=make_icon())
        else:
            if limit > MAX_LIMIT:
                await ctx.send(
                    f"Exceeded the maximum value for amount! The maximum value is {MAX_LIMIT}",
                    ephemeral=True,
                )

                return
            elif limit <= 0:
                await ctx.send(
                    "The amount value can't be less than or equal to 0!", ephemeral=True
                )

                return

            if skip <= 0:
                await ctx.send(
                    "The starting number can't be less than or equal to 0!",
                    ephemeral=True,
                )

                return

            history = await read_history(skip, limit)
            history_entry = []

            async def callback(index, item):
                prompter_mention = await get_user_mention(
                    self.bot, item["prompterUserId"]
                )
                history_entry.append(
                    f"{index}. Prompted by {prompter_mention} - **{item['difficulty']}** difficulty\nfinished at • <t:{item['createdStamp']}:F> | ID: `{item['historyId']}`"
                )

            await use_enumerate(history, callback, skip)

            embed_description = "\n\n".join(history_entry) or "Empty :("
            embed_footer = (
                f"Showing {limit} results | Skipping from {skip}"
                if skip != 1
                else f"Showing {limit} results "
            )
            embed = make_embed(
                "Game History",
                embed_description,
                BOT_COLOR,
            )
            embed.set_footer(
                text=embed_footer,
                icon_url="attachment://icon.png",
            )

            await ctx.send(embed=embed, file=make_icon())


async def setup(bot):
    await bot.add_cog(History(bot))
