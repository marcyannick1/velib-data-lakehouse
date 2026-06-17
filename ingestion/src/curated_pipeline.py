from curated_processor import (
    build_station_dimension,
    build_station_status_fact
)

from storage import upload_dataframe_parquet



def process_curated(staging_data):


    for dataset_name, df in staging_data.items():


        if dataset_name == "station_information":

            curated_df = build_station_dimension(
                df
            )

        else:

            curated_df = build_station_status_fact(
                df
            )


        upload_dataframe_parquet(
            dataset_name,
            curated_df
        )


        print(
            f"Curated saved : {dataset_name}"
        )