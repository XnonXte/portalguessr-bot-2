from discord.ext import commands


async def check_is_owner(ctx_id, owner_id):
    if ctx_id != owner_id:
        raise commands.NotOwner(f"Author's ID ({ctx_id}) is not equal to {owner_id}")
