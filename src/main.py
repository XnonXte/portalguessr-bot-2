"""
The MIT License (MIT)

Copyright (c) 2023-Present XnonXte

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""


import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from const import BOT_PREFIX, BOT_STATUS

load_dotenv("./config.env")

BOT_TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True
bot_activity = discord.Activity(
    type=discord.ActivityType.playing, name=f"{BOT_PREFIX} | {BOT_STATUS}"
)
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


if __name__ == "__main__":
    bot.run(BOT_TOKEN)
