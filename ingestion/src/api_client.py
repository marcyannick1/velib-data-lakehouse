import requests

class VelibAPIClient:

    def get_json(self, url: str):

        response = requests.get(
            url,
            timeout=30
        )

        response.raise_for_status()

        return response.json()