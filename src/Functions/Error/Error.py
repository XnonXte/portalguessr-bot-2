from discord.ext import commands
from hooks.discord.make_embed import make_embed
from config import DANGER_COLOR, DISCORD_INVITE, BOT_PREFIX


class Error(commands.Cog):
    """Cog for error related listener, such as error handler for command error.

    Args:
        commands (commands.Bot): the bot's instance.
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send(
                f"Unknown command: `{ctx.message.content[len(BOT_PREFIX):]}`"
            )
        elif isinstance(error, commands.NoPrivateMessage):
            await ctx.send("This command can only be used inside a server!")
        elif isinstance(error, commands.NotOwner):
            await ctx.send(
                embed=make_embed("Forbidden command!", f"```{error}```", DANGER_COLOR)
            )
        elif isinstance(error, commands.MissingRequiredAttachment):
            await ctx.send(
                embed=make_embed(
                    "Missing required attachment!", f"```{error}```", DANGER_COLOR
                )
            )
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(
                embed=make_embed(
                    "Missing required argument(s)!", f"```{error}```", DANGER_COLOR
                )
            )
        elif isinstance(error, commands.BadLiteralArgument):
            await ctx.send(
                embed=make_embed("Invalid argument(s)!", f"```{error}```", DANGER_COLOR)
            )
        elif isinstance(error, commands.GuildNotFound):
            await ctx.send(
                embed=make_embed(
                    "This command must be invoked in the testing server!",
                    f"Join our testing server: {DISCORD_INVITE}",
                    DANGER_COLOR,
                ),
            )
        elif isinstance(error, commands.UserNotFound):
            await ctx.send(
                embed=make_embed("User not found!", f"```{error}```", DANGER_COLOR)
            )
        elif isinstance(error, commands.BadArgument):
            await ctx.send(
                embed=make_embed("Bad argument!", f"```{error}```", DANGER_COLOR)
            )
        else:
            await ctx.send(
                embed=make_embed("Uncaught error!", f"```{error}```", DANGER_COLOR)
            )
            raise error


async def setup(bot):
    await bot.add_cog(Error(bot))
