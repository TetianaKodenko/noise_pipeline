from datetime import datetime # Import datetime to set the start date for the pipeline
from datetime import timedelta # Import timedelta to specify the duration of retry delays
from airflow import DAG # Import the main DAG class to define our workflow
from airflow.providers.dbt.cloud.operators.dbt import DbtCloudRunJobOperator # Import the specific operator to trigger jobs in dbt Cloud

# Define global settings for all tasks in this DAG
default_args = {
    'retries': 3, # If the task fails, Airflow will automatically retry it 3 times
    'retry_delay': timedelta(minutes=2), # Airflow will wait 2 minutes before each retry attempt
}

# Define the DAG configuration and its timing parameters
with DAG(
    dag_id='dbt_cloud_trigger', # The unique identifier of this workflow inside the Airflow UI
    default_args=default_args, # Pass the retry settings we defined above into the DAG
    start_date=datetime(2026, 1, 1), # The date from which Airflow is allowed to start running this pipeline
    schedule_interval='*/2 * * * *', # Set to None because we want to trigger this workflow manually
    catchup=False, # Disable catching up on missed historical runs
) as dag:

    # Define the specific task that will trigger our production run in dbt Cloud
    trigger_dbt_job = DbtCloudRunJobOperator(
        task_id='trigger_dbt_cloud_job', # The name of this step inside the Airflow workflow graph
        dbt_cloud_conn_id='dbt_cloud_default', # MATCHES YOUR ENVIRONMENT VARIABLE: AIRFLOW_CONN_DBT_CLOUD_DEFAULT
        account_id=70506183133342, # YOUR DBT CLOUD ACCOUNT ID
        job_id=70506183133603, # YOUR PRODUCTION JOB ID
        cause='Airflow trigger', # The comment message that will be shown in dbt Cloud history
    )
