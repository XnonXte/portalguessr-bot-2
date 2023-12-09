import discord


def get_guessr_color(difficulty):
    match difficulty:
        case "Easy":
            return discord.Color.green()
        case "Medium":
            return discord.Color.yellow()
        case "Hard":
            return discord.Color.red()
        case "Very Hard":
            return discord.Color.from_str("000000")
        case _:
            raise Exception("Unknown identifier.")
