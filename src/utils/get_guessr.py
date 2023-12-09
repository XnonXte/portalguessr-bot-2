import requests
import os

import dotenv

from utils.difficulty_converter import diff_expanded_to_acronym

dotenv.load_dotenv("../../.env")

server_uri_endpoint = os.getenv("SERVER_URI")


class GetGuessr:
    def get_all_chambers():
        response = requests.get(f"{server_uri_endpoint}/chambers")

        return response.json()

    def get_random_chambers(amount):
        response = requests.get(f"{server_uri_endpoint}/chambers/random/{amount}")

        return response.json()

    def get_chambers(amount, difficulty):
        difficulty_acronym = diff_expanded_to_acronym(difficulty)
        response = requests.get(
            f"{server_uri_endpoint}/chambers/random/{amount}/{difficulty_acronym}"
        )

        return response.json()
