from hooks.aiohttp.make_request import make_request
from const import SERVER_URL


async def submit_submission(imageUrl, difficulty, answer, submitter, bhHash):
    url = f"{SERVER_URL}/bot/submissions"

    return await make_request(
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


async def read_submission(start, amount, order="desc"):
    url = f"{SERVER_URL}/bot/submissions?start={start}&amount={amount}&order={order}"

    return await make_request(url)


async def read_submission_by_status(status, start, amount, order="desc"):
    url = f"{SERVER_URL}/bot/submissions/status/{status}?start={start}&amount={amount}&order={order}"

    return await make_request(url)


async def read_one_submission(submission_id):
    url = f"{SERVER_URL}/bot/submissions/{submission_id}"

    return await make_request(url)


async def update_submission(submission_id, status):
    url = f"{SERVER_URL}/bot/submissions/{submission_id}"

    return await make_request(url, "PATCH", {"status": status})


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

    return await make_request(
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

    return await make_request(url, "DELETE")
