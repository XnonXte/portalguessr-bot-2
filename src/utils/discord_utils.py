import discord


def make_embed(title=None, description=None, color="#5865F2"):
    return discord.Embed(
        title=title, description=description, color=discord.Color.from_str(color)
    )


def make_file(path, name):
    return discord.File(path, filename=name)
