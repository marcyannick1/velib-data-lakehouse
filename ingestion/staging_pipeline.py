from staging_processor import (
    process_station_information,
    process_station_status
)

from storage import upload_dataframe_csv


def process_staging(snapshots):

    staging_data = {}


    for dataset_name, snapshot in snapshots.items():


        if dataset_name == "station_information":

            df = process_station_information(
                snapshot
            )

        else:

            df = process_station_status(
                snapshot
            )


        upload_dataframe_csv(
            dataset_name,
            df
        )


        staging_data[dataset_name] = df


        print(
            f"Staging saved : {dataset_name}"
        )


    return staging_data