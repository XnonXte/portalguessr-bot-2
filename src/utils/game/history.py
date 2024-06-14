from hooks.aiohttp.make_request import make_request
from config import SERVER_URL


async def read_history(start, amount, order="desc"):
    return await make_request(
        f"{SERVER_URL}/bot/histories?start={start}&amount={amount}&order={order}"
    )


async def read_one_history(history_id):
    return await make_request(f"{SERVER_URL}/bot/histories/{history_id}")


async def add_history(
    total,
    solved,
    timeout,
    skipped,
    mvp,
    participators,
    chambers,
    prompterUserId,
    difficulty,
):
    data = {
        "total": total,
        "solved": solved,
        "timeout": timeout,
        "skipped": skipped,
        "mvp": mvp,
        "participators": participators,
        "chambers": chambers,
        "prompterUserId": prompterUserId,
        "difficulty": difficulty,
    }
    response = await make_request(f"{SERVER_URL}/bot/histories", "POST", data)
    return response["historyId"]


async def remove_history(historyId):
    response = await make_request(f"{SERVER_URL}/histories/{historyId}", "DELETE")
    return response["acknowledged"] == True
