from hooks.web_requests.use_aiohttp import use_aiohttp
from utils.guessr.utils import diff_to_acronym
from const import SERVER_URL


async def get_all_chambers():
    url = f"{SERVER_URL}/chambers"

    return await use_aiohttp(url)


async def get_random_chambers(amount):
    url = f"{SERVER_URL}/chambers/random/{amount}"

    return await use_aiohttp(url)


async def get_chambers(amount, difficulty):
    difficulty_acronym = diff_to_acronym(difficulty)
    url = f"{SERVER_URL}/chambers/random/{amount}/{difficulty_acronym}"

    return await use_aiohttp(url)
