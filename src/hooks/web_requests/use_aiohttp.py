import aiohttp
import os

API_KEY = os.getenv("API_KEY")


async def use_aiohttp(url, method="GET", data=None, headers={"x-api-key": API_KEY}):
    async with aiohttp.ClientSession() as session:
        async with session.request(
            method,
            url,
            json=data,
            headers=headers if method in ["POST", "PATCH", "DELETE"] else None,
        ) as response:
            if response.status < 400:
                return await response.json()
            else:
                raise Exception(f"Error: {response.status} - {await response.text()}")
