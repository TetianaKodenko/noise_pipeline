-- This model filters data based on the latest available record time in the database to avoid timezone and parsing issues
{{ config(materialized='table') }} -- Tells dbt to create a real table in Snowflake

SELECT
    RECORD_DATE, -- The date when the noise level was recorded
    RECORD_TIME, -- The time when the noise level was recorded
    NOISE_LEVEL  -- The measured noise value from the mobile app
FROM {{ source('snowflake_raw', 'NOISE_DATA') }} -- References the source we defined in sources.yml
-- Keeps only the records that are within 10 minutes from the maximum timestamp found in the table
WHERE TIMESTAMP_FROM_PARTS(RECORD_DATE, RECORD_TIME) >= TIMEADD(
    minute, 
    -10, 
    (SELECT MAX(TIMESTAMP_FROM_PARTS(RECORD_DATE, RECORD_TIME)) FROM {{ source('snowflake_raw', 'NOISE_DATA') }})
)