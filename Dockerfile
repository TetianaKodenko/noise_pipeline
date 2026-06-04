FROM quay.io/astronomer/astro-runtime:3.2.4

COPY dags/ /usr/local/airflow/dags/
