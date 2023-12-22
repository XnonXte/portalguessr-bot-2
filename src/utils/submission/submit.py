from hooks.web_requests.use_aiohttp import use_aiohttp
from const import SERVER_URL


async def submit_submission(imageUrl, difficulty, answer, submitter, bhHash):
    url = f"{SERVER_URL}/bot/submissions"

    return await use_aiohttp(
        url,
        "POST",
        {
            "url": imageUrl,
            "difficulty": difficulty,
            "answer": answer,
            "submitter": submitter,
            "bhHash": bhHash,
        },
    )


async def read_submission():
    url = f"{SERVER_URL}/bot/submissions"

    return await use_aiohttp(url)


async def read_one_submission(submission_id):
    url = f"{SERVER_URL}/bot/submissions/{submission_id}"

    return await use_aiohttp(url)
