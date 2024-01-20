async def use_enumerate(array, callback, start):
    for index, item in enumerate(array, start=start):
        await callback(index, item)
