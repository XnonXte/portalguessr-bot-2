from hooks.web_requests.use_aiohttp import use_aiohttp
from const import SERVER_URL


async def read_history():
    return await use_aiohttp(f"{SERVER_URL}/bot/histories")


async def read_one_history(history_id):
    return await use_aiohttp(f"{SERVER_URL}/bot/histories/{history_id}")


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
    response = await use_aiohttp(f"{SERVER_URL}/bot/histories", "POST", data)

    return response["historyId"]  # Returns the history's id.


async def remove_history(historyId):
    response = await use_aiohttp(f"{SERVER_URL}/histories/{historyId}", "DELETE")

    return response["acknowledged"] == True
