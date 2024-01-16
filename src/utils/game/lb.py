from hooks.aiohttp.make_request import make_request
from const import SERVER_URL


async def get_all_scores():
    url = f"{SERVER_URL}/bot/lb/"

    return await make_request(url)


async def get_score(user_id):
    url = f"{SERVER_URL}/bot/lb/{user_id}"

    return await make_request(url)


async def add_score(user_id, data):
    url = f"{SERVER_URL}/bot/lb/{user_id}"

    return await make_request(url, "POST", data)


async def update_score(user_id, data):
    url = f"{SERVER_URL}/bot/lb/{user_id}"

    return await make_request(url, "PATCH", data)


async def remove_score(user_id):
    url = f"{SERVER_URL}/bot/lb/{user_id}"

    return await make_request(url, "DELETE")


async def update_user_stats(user_id, difficulty):
    user_data = await get_score(user_id)

    if user_data == None:
        initial_scores = {"Easy": 0, "Medium": 0, "Hard": 0, "Very Hard": 0}
        initial_scores[difficulty] += 1

        await add_score(user_id, {"scores": initial_scores})
    else:
        user_data["scores"][difficulty] += 1

        await update_score(user_id, user_data)
