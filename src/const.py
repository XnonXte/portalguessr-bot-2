import discord

# Bot's constants.
BOT_COLOR = discord.Color.from_str("#cb3030")
BOT_COLOR_WHITE = discord.Color.from_str("#ededed")
BOT_VERSION = "v0.0.3"
BOT_PREFIX = "!p"
BOT_STATUS = "portalguessr.vercel.app"

# Guessr's constants.
CHAMBERS = [
    "00",
    "01",
    "02",
    "03",
    "04",
    "05",
    "06",
    "07",
    "08",
    "09",
    "10",
    "11",
    "12",
    "13",
    "14",
    "15",
    "16",
    "17",
    "18",
    "19",
    "e00",
    "e01",
    "e02",
]
EASY_COLOR = discord.Color.from_str("#4caf50")
MEDIUM_COLOR = discord.Color.from_str("#fedc56")
HARD_COLOR = discord.Color.from_str("#ff5733")
VERY_HARD_COLOR = discord.Color.from_str("#36cbd3")

# URLs constants.
SERVER_URL = (
    "https://portalguessr-api.cyclic.app"  # Fill in your own portalguessr-api URL.
)
IMGBB_SERVER_URL = "https://api.imgbb.com/1/upload"

# Embed commands.
GENERAL_COMMANDS = {
    "guess": "Starts a PortalGuessr game",
    "lb": "Shows the current leaderboard",
    "help": "Shows the available commands you can use",
    "submit": "Submits a chamber for the chance of getting added",
    "submissions": "Checks submissions status",
    "history": "Checks recent guessrs history",
}
OWNER_COMMANDS = {
    "accept": "Accepts a pending submission",
    "reject": "Rejects a pending submission",
    "lb_add": "Adds a new stats to the leaderboard",
    "lb_remove": "Removes an existing stats from the leaderboard",
    "review": "Starts a review session for pending submissions.",
}
DEFAULT_FOOTER_TEXT = f"PortalGuessr 2 {BOT_VERSION}"

# Submissions constants.
SUBMISSION_REJECTED = discord.Color.from_str("#99aab5")
SUBMISSION_ACCEPTED = discord.Color.from_str("#57f287")
SUBMISSION_PENDING = discord.Color.from_str("#99aab5")

# Misc constants.
XNONXTE_USER_ID = 706330866267193344
OWNER_USER_ID = 706330866267193344  # Fill in with your own user ID on Discord.
TESTING_SERVER_ID = (
    1103578001318346812  # Fill in with your own testing server's ID on Discord.
)
DISCORD_INVITE = "https://discord.com/invite/dDbgtFb2KC"
DANGER_COLOR = discord.Color.from_str("#FF0000")
