import duckdb

con = duckdb.connect()

input_file = "parquet_data/2021_raw_census_data.parquet"

# Main data
con.execute(f"""
    COPY (
        SELECT DISTINCT
            CENSUS_YEAR,
            DGUID,
            CHARACTERISTIC_ID,
            C1_COUNT_TOTAL,
            "C2_COUNT_MEN+",
            "C3_COUNT_WOMEN+",
            C10_RATE_TOTAL,
            "C11_RATE_MEN+",
            "C12_RATE_WOMEN+"
        FROM '{input_file}'
    )
    TO 'parquet_data/2021_census_data.parquet'
    (FORMAT PARQUET, COMPRESSION ZSTD)
""")

# Characteristics lookup table
con.execute(f"""
    COPY (
        SELECT DISTINCT
            CENSUS_YEAR,
            CHARACTERISTIC_ID,
            CHARACTERISTIC_NAME
        FROM '{input_file}'
        ORDER BY CHARACTERISTIC_ID
    )
    TO 'parquet_data/2021_characteristics.parquet'
    (FORMAT PARQUET, COMPRESSION ZSTD)
""")

# Geography lookup table
con.execute(f"""
    COPY (
        SELECT DISTINCT
            CENSUS_YEAR,
            DGUID,
            GEO_LEVEL,
            GEO_NAME
        FROM '{input_file}'
        ORDER BY DGUID
    )
    TO 'parquet_data/2021_geographies.parquet'
    (FORMAT PARQUET, COMPRESSION ZSTD)
""")

con.close()