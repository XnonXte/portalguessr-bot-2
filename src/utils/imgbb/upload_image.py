import aiohttp
import asyncio
import os

from const import IMGBB_SERVER_URL

IMGBB_API_KEY = os.getenv("IMGBB_API_KEY")


async def upload_image(url, fileName):
    params = {"key": IMGBB_API_KEY}
    data = {"image": (fileName, url)}

    async with aiohttp.ClientSession() as session:
        async with session.post(IMGBB_SERVER_URL, params=params, data=data) as response:
            response_data = await response.json()

    return response_data["data"]["url"]
