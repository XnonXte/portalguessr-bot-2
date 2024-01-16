import discord


async def get_user(bot, user_id):
    try:
        return await bot.fetch_user(int(user_id))
    except ValueError:
        return None
    except discord.NotFound:
        return None
