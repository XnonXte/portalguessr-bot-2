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


async def read_submission_by_status(status):
    url = f"{SERVER_URL}/bot/submissions/status/{status}"

    return await use_aiohttp(url)


async def update_submission(submission_id, status):
    url = f"{SERVER_URL}/bot/submissions/{submission_id}"

    return await use_aiohttp(url, "PATCH", {"status": status})


async def accept_submission(submission_id):
    response = await update_submission(submission_id, "accepted")

    if response == None:
        raise Exception(f"Not found submission ID: {submission_id}!")

    if response["status"] == "accepted":
        raise Exception("You can't accept an already accepted submission!")

    (url, difficulty, answer, bhHash, submitter) = (
        response["url"],
        response["difficulty"],
        response["answer"],
        response["bhHash"],
        response["submitter"],
    )
    new_chamber_url = f"{SERVER_URL}/chambers/new"

    return await use_aiohttp(
        new_chamber_url,
        "POST",
        {
            "url": url,
            "difficulty": difficulty,
            "answer": answer,
            "bhHash": bhHash,
            "submitter": submitter,
        },
    )


async def delete_submission(submission_id):
    url = f"{SERVER_URL}/bot/submissions/{submission_id}"

    return await use_aiohttp(url, "DELETE")
