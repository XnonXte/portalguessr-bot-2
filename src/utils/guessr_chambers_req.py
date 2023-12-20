from utils.use_aiohttp_request import make_aiohttp_req
from utils.guessr_utils import guessr_diff_to_acronym
from const import SERVER_URI


async def guessr_get_all_chambers():
    url = f"{SERVER_URI}/chambers"
    return await make_aiohttp_req(url)


async def guessr_get_random_chambers(amount):
    url = f"{SERVER_URI}/chambers/random/{amount}"
    return await make_aiohttp_req(url)


async def guessr_get_chambers(amount, difficulty):
    difficulty_acronym = guessr_diff_to_acronym(difficulty)
    url = f"{SERVER_URI}/chambers/random/{amount}/{difficulty_acronym}"
    return await make_aiohttp_req(url)
