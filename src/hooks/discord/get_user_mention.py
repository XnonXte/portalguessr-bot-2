import discord


async def get_user_mention(bot, user_id):
    try:
        return (await bot.fetch_user(int(user_id))).mention
    except ValueError:
        return "N/A"
    except discord.NotFound:
        return "Not Found"
