import aiohttp


async def use_aiohttp(url, method="GET", data=None, headers=None):
    async with aiohttp.ClientSession() as session:
        async with session.request(method, url, json=data, headers=headers) as response:
            if response.status < 400:
                return await response.json()
            else:
                raise Exception(f"Error: {response.status} - {await response.text()}")
