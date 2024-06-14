from hooks.aiohttp.make_request import make_request
from config import SERVER_URL


async def get_statistics(start, amount, order="desc"):
    url = f"{SERVER_URL}/bot/lb?start={start}&amount={amount}&order={order}"
    return await make_request(url)


async def get_statistic(user_id):
    url = f"{SERVER_URL}/bot/lb/{user_id}"
    return await make_request(url)


async def add_statistic(user_id, data):
    url = f"{SERVER_URL}/bot/lb/{user_id}"
    return await make_request(url, "POST", data)


async def update_statistic(user_id, data):
    url = f"{SERVER_URL}/bot/lb/{user_id}"
    return await make_request(url, "PATCH", data)


async def remove_statistic(user_id):
    url = f"{SERVER_URL}/bot/lb/{user_id}"
    return await make_request(url, "DELETE")


async def update_user_statistic(user_id, difficulty):
    statistic = await get_statistic(user_id)
    if statistic == None:
        initial_scores = {"Easy": 0, "Medium": 0, "Hard": 0, "Very Hard": 0}
        initial_scores[difficulty] += 1

        await add_statistic(user_id, {"scores": initial_scores})
    else:
        statistic["scores"][difficulty] += 1

        await update_statistic(user_id, statistic)
