import os
import aiohttp
from config import API_KEY


async def make_request(
    url, method="GET", json=None, headers=None, params=None, data=None
):
    async with aiohttp.ClientSession() as session:
        async with session.request(
            method,
            url,
            json=json,
            params=params,
            data=data,
            headers=(
                headers
                if method not in ["POST", "PATCH", "DELETE"]
                else {"x-api-key": API_KEY}
            ),
        ) as response:
            if response.ok:
                return await response.json()
            else:
                raise Exception(f"Error: {response.status} - {await response.text()}")
