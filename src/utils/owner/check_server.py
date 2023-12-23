from discord.ext import commands


async def check_is_testing_server(server_id, testing_server_id):
    if server_id != testing_server_id:
        raise commands.GuildNotFound(
            f"Server's ID ({server_id}) is not equal to {testing_server_id}"
        )
