from api_client import VelibAPIClient
from datetime import datetime
from storage import upload_raw_snapshot


SOURCES = {
    "station_information":
        "https://velib-metropole-opendata.smovengo.cloud/opendata/Velib_Metropole/station_information.json",

    "station_status":
        "https://velib-metropole-opendata.smovengo.cloud/opendata/Velib_Metropole/station_status.json"
}


class Extractor:

    @staticmethod
    def build_snapshot(data):

        return {
            "extracted_at": datetime.utcnow().isoformat(),
            "data": data
        }


def extract():

    client = VelibAPIClient()

    snapshots = {}

    for dataset_name, url in SOURCES.items():

        print(f"Extracting {dataset_name}")

        data = client.get_json(url)

        snapshot = Extractor.build_snapshot(
            data
        )

        upload_raw_snapshot(
            dataset_name,
            snapshot
        )

        snapshots[dataset_name] = snapshot

        print(
            f"Raw saved : {dataset_name}"
        )

    return snapshots