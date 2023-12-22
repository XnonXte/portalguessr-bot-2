import requests
import os

from const import IMGBB_SERVER_URL

IMGBB_API_KEY = os.getenv("IMGBB_API_KEY")


def upload_image(url, fileName):
    params = {"key": IMGBB_API_KEY}
    data = {"image": (fileName, url)}

    request = requests.post(IMGBB_SERVER_URL, params=params, data=data)
    response = request.json()

    return response["data"]["url"]
