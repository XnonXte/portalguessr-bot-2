import aiohttp


async def use_aiohttp(url, method="GET", data=None):
    async with aiohttp.ClientSession() as session:
        async with session.request(method, url, json=data) as response:
            if response.status < 400:
                return await response.json()
            else:
                raise Exception(
                    f"Response status at 400 or higher - {await response.json()}"
                )
