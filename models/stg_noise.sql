WITH raw_data AS (
    -- Pull the initial raw data directly from the source table
    SELECT * FROM NOISE_DB.NOISE_SCHEMA.NOISE_DATA
),

deduplicated AS (
    -- Remove duplicate rows, keeping 1 record per exact second
    SELECT *
    FROM raw_data
    QUALIFY ROW_NUMBER() OVER(PARTITION BY DATE_TIME ORDER BY NOISE_LEVEL) = 1
),

cleaned_data AS (
    -- Fix missing values (NULLs) by replacing them with the median noise for that specific minute
    SELECT
        DATE_TIME,
        COALESCE(
            NOISE_LEVEL,
            MEDIAN(NOISE_LEVEL) OVER(PARTITION BY DATE_TRUNC('MINUTE', DATE_TIME))
        ) AS NOISE_LEVEL
    FROM deduplicated
)

-- Pull the final result
SELECT * FROM cleaned_data