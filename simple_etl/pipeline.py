from time import sleep
import pandas as pd

from openhexa.sdk import current_run, pipeline


@pipeline("simple-etl")
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
    sleep(4)  # Let's pretend we are querying an external system

    return pd.DataFrame([{"id": 1, "person": 1, "activity": "Activity 1"},
                         {"id": 1, "person": 1, "activity": "Activity 1"},
                         {"id": 1, "person": 1, "activity": "Activity 2"},
                         {"id": 1, "person": 1, "activity": "Activity 3"},
                         {"id": 1, "person": 2, "activity": "Activity 2"},
                         {"id": 2, "person": 2, "activity": "Activity 3"},
                         {"id": 2, "person": 3, "activity": "Activity 1"},
                         {"id": 2, "person": 3, "activity": "Activity 2"}]).set_index("id")


@simple_etl.task
def transform(people_data, activity_data):
    current_run.log_info(f"Transforming data...")
    combined_df = activity_data.join(people_data, on="person").reset_index()

    return combined_df


@simple_etl.task
def load(transformed_data):
    current_run.log_info(f"Loading data ({len(transformed_data)} records)")


if __name__ == "__main__":
    simple_etl()