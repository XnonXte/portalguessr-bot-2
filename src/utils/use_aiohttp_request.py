import aiohttp


async def make_aiohttp_req(url, method="GET", data=None):
    async with aiohttp.ClientSession() as session:
        async with session.request(method, url, json=data) as response:
            if response.status == 200:
                return await response.json()
            else:
                raise Exception(
                    f"Not 'ok' response code returned: {response.status} - {response.reason}"
                )
