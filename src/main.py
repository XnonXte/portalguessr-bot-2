# TODO: Implement an elo system.
# TODO: Add owner-only commands.
# TODO: Daily PortalGuessr would be so cool!
# TODO: Auto assigned roles for top guessrs?
# TODO: Migrate into using pipenv.

import os
from typing import Literal, Optional

import discord
from discord.ext import commands
from dotenv import load_dotenv

from misc.replit import keep_alive

load_dotenv("./config.env")

PREFIX = os.getenv("PREFIX")
BOT_TOKEN = os.getenv("TOKEN")
BOT_PREFIX = commands.when_mentioned_or(PREFIX)
BOT_STATUS = os.getenv("STATUS")

intents = discord.Intents.default()
intents.message_content = True


class PortalGuessr2(commands.Bot):
    async def setup_hook(self):
        for function in os.listdir("./src/Functions"):
            for cog in os.listdir(f"./src/Functions/{function}"):
                if cog.endswith(".py") and cog != "__init__.py":
                    await self.load_extension(
                        f"Functions.{function}.{cog[:-3]}"
                    )  # Excluding .py


bot = PortalGuessr2(command_prefix=BOT_PREFIX, intents=intents, help_command=None)


@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}!")

    await bot.change_presence(
        activity=discord.Activity(type=discord.ActivityType.playing, name=BOT_STATUS)
    )


@bot.event
async def on_command_error(ctx: commands.Context, error: commands.CommandError):
    # Error handler.
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f"Unknown command: `{ctx.message.content[len(PREFIX):]}`")
    if isinstance(error, commands.NotOwner):
        await ctx.send("Forbidden command! You're not the owner of this bot!")
    else:
        raise error


@bot.command()
@commands.guild_only()
@commands.is_owner()
async def sync(
    ctx: commands.Context,
    guilds: commands.Greedy[discord.Object],
    spec: Optional[Literal["~", "*", "^"]] = None,
) -> None:
    # Command I stole from Github.
    if not guilds:
        if spec == "~":
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "*":
            ctx.bot.tree.copy_global_to(guild=ctx.guild)
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "^":
            ctx.bot.tree.clear_commands(guild=ctx.guild)
            await ctx.bot.tree.sync(guild=ctx.guild)
            synced = []
        else:
            synced = await ctx.bot.tree.sync()

        await ctx.send(
            f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
        )
        return

    ret = 0
    for guild in guilds:
        try:
            await ctx.bot.tree.sync(guild=guild)
        except discord.HTTPException:
            pass
        else:
            ret += 1

    await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")


keep_alive()
bot.run(BOT_TOKEN)
