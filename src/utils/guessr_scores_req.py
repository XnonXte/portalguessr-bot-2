from utils.use_aiohttp_request import make_aiohttp_req
from const import SERVER_URI


async def guessr_get_all_scores():
    url = f"{SERVER_URI}/bot/lb/"
    return await make_aiohttp_req(url)


async def guessr_get_score(user_id):
    url = f"{SERVER_URI}/bot/lb/{user_id}"
    return await make_aiohttp_req(url)


async def guessr_add_score(user_id, data):
    url = f"{SERVER_URI}/bot/lb/{user_id}"
    return await make_aiohttp_req(url, "POST", data)


async def guessr_update_score(user_id, data):
    url = f"{SERVER_URI}/bot/lb/{user_id}"
    return await make_aiohttp_req(url, "PATCH", data)


async def guessr_remove_score(user_id):
    url = f"{SERVER_URI}/bot/lb/{user_id}"
    return await make_aiohttp_req(url, "DELETE")
