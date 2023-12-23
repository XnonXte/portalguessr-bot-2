import os
from typing import Literal, Optional

import discord
from discord.ext import commands
from dotenv import load_dotenv

from misc.replit import keep_alive
from hooks.discord.use_discord import make_embed
from const import BOT_PREFIX, BOT_STATUS

load_dotenv("./config.env")

BOT_TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot_activity = discord.Activity(type=discord.ActivityType.playing, name=BOT_STATUS)
bot_status = discord.Status.do_not_disturb


class PortalGuessr2(commands.Bot):
    async def setup_hook(self):
        for function in os.listdir("./src/Functions"):
            for cog in os.listdir(f"./src/Functions/{function}"):
                if cog.endswith(".py") and cog != "__init__.py":
                    await self.load_extension(
                        f"Functions.{function}.{cog[:-3]}"
                    )  # Excluding .py


bot = PortalGuessr2(
    command_prefix=BOT_PREFIX,
    intents=intents,
    help_command=None,
    activity=bot_activity,
    status=bot_status,
)


@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}!")


@bot.event
async def on_command_error(ctx: commands.Context, error: commands.CommandError):
    # Error handler.
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f"Unknown command: `{ctx.message.content[len(BOT_PREFIX):]}`")
    elif isinstance(error, commands.NotOwner):
        await ctx.send(
            embed=make_embed(
                "You're not the owner of this bot!", f"```{error}```", "#FF0000"
            )
        )
    elif isinstance(error, commands.MissingRequiredAttachment):
        await ctx.send(
            embed=make_embed(
                "Missing required attachment!", f"```{error}```", "#FF0000"
            )
        )
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(
            embed=make_embed(
                "Missing required argument(s)!", f"```{error}```", "#FF0000"
            )
        )
    else:
        await ctx.send(embed=make_embed("Uncaught Error!", f"```{error}```", "#FF0000"))

        raise error


@bot.command()
@commands.is_owner()
async def sync(ctx: commands.Context, target: Optional[Literal["*", ".", "-"]] = "*"):
    if target == "*":
        synced = await ctx.bot.tree.sync()
    elif target == "-":
        ctx.bot.tree.clear_commands(guild=ctx.guild)
        await ctx.bot.tree.sync(guild=ctx.guild)
        synced = []
    else:
        ctx.bot.tree.copy_global_to(guild=ctx.guild)
        synced = await ctx.bot.tree.sync(guild=ctx.guild)

    await ctx.send(
        f"Synced {len(synced)} commands {'globally' if target == '*' else 'to the current guild.'}"
    )


keep_alive()
bot.run(BOT_TOKEN)
