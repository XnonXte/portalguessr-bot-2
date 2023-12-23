from hooks.discord.use_discord import make_file


# Bot's constants.
BOT_COLOR = "#cb3030"
BOT_VERSION = "v0.0.1"
BOT_PREFIX = "!p"
BOT_STATUS = "portalguessr.vercel.app"
BOT_MAKE_ICON = lambda: make_file(
    "./src/assets/icon.png", "icon.png"
)  # Apparently a constant KEKW.

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
EASY_COLOR = "#4caf50"
MEDIUM_COLOR = "#fedc56"
HARD_COLOR = "#ff5733"
VERY_HARD_COLOR = "#36cbd3"

# URLs constants.
SERVER_URL = "https://portalguessr-api.cyclic.app"
IMGBB_SERVER_URL = "https://api.imgbb.com/1/upload"

# Embed commands.
GENERAL_COMMANDS = {
    "guess": "Starts a PortalGuessr game",
    "lb": "Shows the current leaderboard",
    "help": "Shows the available commands you can use",
    "submit": "Submits a chamber for the chance of getting added",
    "status": "Sees the submission status",
    "history": "Checks recent guessrs history",
}
OWNER_COMMANDS = {
    "accept": "Accepts a pending submission",
    "reject": "Rejects a pending submission",
    "lb_add": "Adds a new stats to the leaderboard",
    "lb_remove": "Removes an existing stats from the leaderboard.",
}
DEFAULT_FOOTER_TEXT = f"PortalGuessr 2 {BOT_VERSION}"

# Misc constants.
XNONXTE_USER_ID = 706330866267193344
OWNER_USER_ID = 706330866267193344  # Fill in with your own user ID on Discord.
