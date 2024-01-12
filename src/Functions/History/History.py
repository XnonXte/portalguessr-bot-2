from typing import Optional
from datetime import datetime

from discord.ext import commands
from discord import app_commands

from hooks.discord.use_discord import make_embed, get_user_mention, get_user
from utils.guessr.history import read_history, read_one_history
from utils.bot.utils import bot_make_icon
from const import BOT_COLOR, MAX_AMOUNT


class History(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(
        name="history", description="Checks recent guessrs history."
    )
    @app_commands.describe(
        history_id="Targets a specific game from history with its ID.",
        start="The starting index (one-based index).",
        amount=f"The total amount that needs to be displayed (max: {MAX_AMOUNT}",
    )
    async def history(
        self,
        ctx: commands.Context,
        history_id: Optional[str],
        start: Optional[int] = 1,
        amount: Optional[int] = 10,
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

                await ctx.send(embed=embed, file=bot_make_icon())
        else:
            history = await read_history()
            history_length = len(history)

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

            if history_length != 0:
                if start > history_length:
                    await ctx.send(
                        f"Start value cannot exceed {history_length}!",
                        ephemeral=True,
                    )

                    return
                elif start <= 0:
                    await ctx.send(
                        "Starting index cannot be less than 0!",
                        ephemeral=True,
                    )

                    return

            adjusted_amount = (
                (start + amount) - 1
                if not start + amount > history_length
                else history_length
            )
            adjusted_end_index = (
                adjusted_amount if start - 1 != history_length else adjusted_amount + 1
            )
            history_reversed = history[::-1]
            history_entry = []

            for index, game in enumerate(history_reversed, start=1):
                entry_message = f"{index}. **{game['solved']}** solved, **{game['timeout']}** timed out, **{game['skipped']}** skipped, **{game['total']}** total, **{game['difficulty']}** difficulty\nfinished at • <t:{game['createdStamp']}:F> | ID: `{game['historyId']}`"
                history_entry.append(entry_message)

            data_entry = history_entry[start - 1 : adjusted_end_index]
            data_entry_length = len(data_entry)
            embed_description = "\n\n".join(data_entry) or "Empty :("

            embed = make_embed(
                "Game History",
                embed_description,
                BOT_COLOR,
            )
            embed.set_footer(
                text=f"Showing {data_entry_length} out of {history_length} total.",
                icon_url="attachment://icon.png",
            )

            await ctx.send(embed=embed, file=bot_make_icon())


async def setup(bot):
    await bot.add_cog(History(bot))
