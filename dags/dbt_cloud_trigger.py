from datetime import datetime # Import datetime to set the start date for the pipeline
from datetime import timedelta # Import timedelta to specify the duration of retry delays
from airflow import DAG # Import the main DAG class to define our workflow
from airflow.operators.python import ShortCircuitOperator # Import the operator to stop execution outside specified hours
from airflow.providers.dbt.cloud.operators.dbt import DbtCloudRunJobOperator # Import the specific operator to trigger jobs in dbt Cloud

def check_time_window(**context):
    now = context['data_interval_start']
    # Restrict execution to the 21:00 - 21:15 time window daily
    return now.hour == 21 and 0 <= now.minute <= 15

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
    schedule='*/2 21 * * *', # Modified cron to trigger every 2 minutes only during the 21:00-21:58 hour window
    catchup=False, # Disable catching up on missed historical runs
) as dag:

    # Task to verify if the current execution sits precisely between 21:00 and 21:15
    gatekeeper = ShortCircuitOperator(
        task_id='check_time_window',
        python_callable=check_time_window
    )

    # Define the specific task that will trigger our production run in dbt Cloud
    trigger_dbt_job = DbtCloudRunJobOperator(
        task_id='trigger_dbt_cloud_job', # The name of this step inside the Airflow workflow graph
        dbt_cloud_conn_id='dbt_cloud_default', # MATCHES YOUR ENVIRONMENT VARIABLE: AIRFLOW_CONN_DBT_CLOUD_DEFAULT
        account_id=70506183133342, # YOUR DBT CLOUD ACCOUNT ID
        job_id=70506183132733, # YOUR PRODUCTION JOB ID
        trigger_reason='Airflow trigger', # The comment message that will be shown in dbt Cloud history
    ) 

    # Set execution dependency: gatekeeper evaluates first, then triggers dbt Cloud if True
    gatekeeper >> trigger_dbt_job
