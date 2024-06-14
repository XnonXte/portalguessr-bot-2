import os
import discord
import dotenv

# Load environment variables.
dotenv.load_dotenv("./.env")

# Environment variables.
TOKEN = os.getenv("TOKEN")
SERVER_URL = os.getenv("SERVER_URL")
IMGBB_SERVER_URL = os.getenv("IMGBB_SERVER_URL")
DISCORD_INVITE = os.getenv("DISCORD_INVITE")
INVITE_URL = os.getenv("INVITE_URL")
SUBMISSION_CHANNEL_ID = int(os.getenv("SUBMISSION_CHANNEL_ID"))
OWNER_USER_ID = int(os.getenv("OWNER_USER_ID"))
TESTING_SERVER_ID = int(os.getenv("TESTING_SERVER_ID"))
P1SR_GUILD_ID = int(os.getenv("P1SR_GUILD_ID"))
P1SR_SPAM_CHANNEL_ID = int(os.getenv("P1SR_SPAM_CHANNEL_ID"))
API_KEY = os.getenv("API_KEY")

# Bot constants.
BOT_VERSION = "v0.0.7"
BOT_PREFIX = "!p"
BOT_STATUS = "portalguessr.vercel.app"
BOT_FOOTER_TEXT = f"PortalGuessr 2 {BOT_VERSION}"

# Game constant.
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


# Commands information.
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


# Color constants.
BOT_ACCENT_COLOR = discord.Color.from_str("#cb3030")
BOT_ACCENT_COLOR_WHITE = discord.Color.from_str("#ededed")
SUBMISSION_REJECTED = discord.Color.from_str("#99aab5")
SUBMISSION_ACCEPTED = discord.Color.from_str("#57f287")
SUBMISSION_PENDING = discord.Color.from_str("#99aab5")
EASY_COLOR = discord.Color.from_str("#4caf50")
MEDIUM_COLOR = discord.Color.from_str("#fedc56")
HARD_COLOR = discord.Color.from_str("#ff5733")
VERY_HARD_COLOR = discord.Color.from_str("#36cbd3")
DANGER_COLOR = discord.Color.from_str("#FF0000")

# Limit constants.
MAX_REQUEST_ENTRIES = 20
DEFAULT_REQUEST_ENTRIES = 10
MAX_GUESSR_ROUNDS = 25

# Misc.
GITHUB_URL = "https://github.com/XnonXte/portalguessr-bot-2"
