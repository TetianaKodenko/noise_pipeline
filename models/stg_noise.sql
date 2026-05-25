WITH raw_data AS (
    -- This CTE is needed to pull the initial raw data directly from your source table in Snowflake.
    SELECT * FROM NOISE_DB.NOISE_SCHEMA.NOISE_DATA
),

deduplicated AS (
    -- This CTE is needed to remove duplicate rows.
    -- It takes data from 'raw_data' and keeps only 1 record per exact second, in case the phone sent multiple records at the same time.
    SELECT *
    FROM raw_data
    QUALIFY ROW_NUMBER() OVER(PARTITION BY RECORD_DATE, RECORD_TIME ORDER BY NOISE_LEVEL) = 1
),

cleaned_data AS (
    -- This CTE is needed to fix missing values (NULLs).
    -- It takes data from 'deduplicated' and replaces any empty noise level with the median noise for that specific minute.
    SELECT
        RECORD_DATE,
        RECORD_TIME,
        COALESCE(
            NOISE_LEVEL,
            MEDIAN(NOISE_LEVEL) OVER(PARTITION BY RECORD_DATE, MINUTE(RECORD_TIME))
        ) AS NOISE_LEVEL
    FROM deduplicated
)

-- This pulls the final result from the 'cleaned_data' CTE.
SELECT * FROM cleaned_data