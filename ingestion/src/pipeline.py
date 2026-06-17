from extract_pipeline import extract
from staging_pipeline import process_staging
from curated_pipeline import process_curated



def run_pipeline():

    snapshots = extract()

    staging = process_staging(
        snapshots
    )

    process_curated(
        staging
    )