-- This model filters the raw noise data to keep only the records from the last 10 minutes
{{ config(materialized='table') }} -- Tells dbt to create a real table in Snowflake, not just a view

SELECT
    RECORD_DATE, -- The date when the noise level was recorded
    RECORD_TIME, -- The time when the noise level was recorded
    NOISE_LEVEL  -- The measured noise value from the mobile app
FROM {{ source('snowflake_raw', 'NOISE_DATA') }} -- References the source we defined in sources.yml
WHERE RECORD_TIME >= TIMEADD(minute, -10, CURRENT_TIME()) -- Keeps only data from the last 10 minutes