import discord


def make_file(path, name):
    return discord.File(path, filename=name)
