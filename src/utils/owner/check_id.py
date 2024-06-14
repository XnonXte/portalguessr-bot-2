from discord.ext import commands
from config import OWNER_USER_ID


def check_is_owner(ctx_id):
    if ctx_id != OWNER_USER_ID:
        raise commands.NotOwner(
            f"Author's ID ({ctx_id}) is not equal to {OWNER_USER_ID}"
        )
