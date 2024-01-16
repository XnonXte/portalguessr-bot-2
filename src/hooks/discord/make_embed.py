import discord


def make_embed(title=None, description=None, color=discord.Color.blurple()):
    return discord.Embed(title=title, description=description, color=color)
