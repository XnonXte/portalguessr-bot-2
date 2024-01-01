import discord


def make_embed(title=None, description=None, color=discord.Color.blurple):
    return discord.Embed(title=title, description=description, color=color)


def make_file(path, name):
    return discord.File(path, filename=name)


async def get_user_mention(bot, user_id):
    try:
        return (await bot.fetch_user(int(user_id))).mention
    except ValueError:
        return "N/A"
    except discord.NotFound:
        return "Not Found"


async def get_user(bot, user_id):
    try:
        return await bot.fetch_user(int(user_id))
    except ValueError:
        return None
    except discord.NotFound:
        return None
