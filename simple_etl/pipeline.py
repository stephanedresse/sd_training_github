import json
from time import sleep
import pandas as pd

from openhexa.sdk import current_run, pipeline, workspace
from sqlalchemy import create_engine, Integer, String


@pipeline("simple-etl", timeout=10)  # Timeout in seconds)
def simple_etl():
    people_data = extract_people_data()
    activity_data = extract_activity_data()
    transformed_data = transform(people_data, activity_data)
    load(transformed_data)


@simple_etl.task
def extract_people_data():
    current_run.log_info("Extracting people data...")
    sleep(2)  # Let's pretend we are querying an external system

    return pd.DataFrame([{"id": 1, "first_name": "Mary", "last_name": "Johnson"},
                         {"id": 2, "first_name": "Peter", "last_name": "Jackson"},
                         {"id": 3, "first_name": "Taylor", "last_name": "Smith"}]).set_index("id")


@simple_etl.task
def extract_activity_data():
    current_run.log_info(f"Extracting activity data...")
    with open(f"{workspace.files_path}/activities.json", "r") as activities_file:
        return pd.DataFrame(json.load(activities_file)["activities"]).set_index("id")


@simple_etl.task
def transform(people_data, activity_data):
    current_run.log_info(f"Transforming data...")
    combined_df = activity_data.join(people_data, on="person").reset_index()

    return combined_df


@simple_etl.task
def load(transformed_data):
    current_run.log_info(f"Loading data ({len(transformed_data)} records)")

    output_path = f"{workspace.files_path}/transformed.csv"
    transformed_data.to_csv(output_path)
    current_run.add_file_output(output_path)

    engine = create_engine(workspace.database_url)
    
    # Let's use chunksize to control memory usage, and dtype to avoid weird casting issues
    transformed_data.to_sql("transformed", if_exists="replace", con=engine,
                            chunksize=100, dtype={"id": Integer(), "first_name": String(), "last_name": String()})
    current_run.add_database_output("transformed")


if __name__ == "__main__":
    simple_etl()