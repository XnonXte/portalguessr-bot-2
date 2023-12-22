from hooks.web_requests.use_aiohttp import use_aiohttp
from const import SERVER_URL


async def get_all_scores():
    url = f"{SERVER_URL}/bot/lb/"

    return await use_aiohttp(url)


async def get_score(user_id):
    url = f"{SERVER_URL}/bot/lb/{user_id}"

    return await use_aiohttp(url)


async def add_score(user_id, data):
    url = f"{SERVER_URL}/bot/lb/{user_id}"

    return await use_aiohttp(url, "POST", data)


async def update_score(user_id, data):
    url = f"{SERVER_URL}/bot/lb/{user_id}"

    return await use_aiohttp(url, "PATCH", data)


async def remove_score(user_id):
    url = f"{SERVER_URL}/bot/lb/{user_id}"

    return await use_aiohttp(url, "DELETE")
