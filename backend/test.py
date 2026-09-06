import zipfile
import pandas as pd
import re
import os
import numpy as np

import duckdb

con = duckdb.connect()


# preprocess 2016 census data
input_file = 'temp_parquet_data/2016_raw_census_data.parquet'

con.execute("""
    CREATE TABLE IF NOT EXISTS data_2016 (
        CENSUS_YEAR INTEGER,
        GEO_CODE INTEGER,
        CHARACTERISTIC_ID INTEGER,
        COUNT_TOTAL DOUBLE,
        COUNT_MALE DOUBLE,
        COUNT_FEMALE DOUBLE
    );
""")

# Copy counts from the original parquet file
con.execute(f"""
    INSERT INTO data_2016
    SELECT DISTINCT
        CENSUS_YEAR,
        GEO_CODE,
        CHARACTERISTIC_ID,
        COUNT_TOTAL,
        COUNT_MALE,
        COUNT_FEMALE
    FROM '{input_file}';
""")

# create temporary table with characteristic 8 to get the rates
# Characteristic id 8 has total 2016 population
con.execute(f"""
    CREATE TEMP TABLE population_2016 AS
    SELECT
        GEO_CODE,
        COUNT_TOTAL AS TOTAL_POPULATION,
        COUNT_MALE AS MALE_POPULATION,
        COUNT_FEMALE AS FEMALE_POPULATION
    FROM '{input_file}'
    WHERE CHARACTERISTIC_ID = 8;
""").fetchdf()

res = con.execute(f"""
    SELECT
        d.CHARACTERISTIC_ID,
        d.COUNT_TOTAL * 100.0 / NULLIF(p.TOTAL_POPULATION, 0)
            AS RATE_TOTAL
    FROM data_2016 AS d
    LEFT JOIN population_2016 p
        ON d.GEO_CODE = p.GEO_CODE
    WHERE d.GEO_CODE=0;
""").fetchdf()

con.close()


print(res)