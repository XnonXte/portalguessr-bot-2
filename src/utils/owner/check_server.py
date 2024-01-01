from discord.ext import commands

from const import TESTING_SERVER_ID


def check_is_testing_server(server_id):
    if server_id != TESTING_SERVER_ID:
        raise commands.GuildNotFound(
            f"Server's ID ({server_id}) is not equal to {TESTING_SERVER_ID}"
        )
