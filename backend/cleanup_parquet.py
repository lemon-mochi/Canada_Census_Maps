import duckdb

con = duckdb.connect()

# start with 2021 census data

input_file = "temp_parquet_data/2021_raw_census_data.parquet"

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

# List of data columns
con.execute("""
    CREATE TABLE column_values (
        column_id INTEGER PRIMARY KEY,
        column_name VARCHAR
    );
""")

con.execute("""
    INSERT INTO column_values VALUES
        (1, 'C1_COUNT_TOTAL'),
        (2, 'C2_COUNT_MEN+'),
        (3, 'C3_COUNT_WOMEN+'),
        (4, 'C10_RATE_TOTAL'),
        (5, 'C11_RATE_MEN+'),
        (6, 'C12_RATE_WOMEN+');
""")

columns = [
    "C1_COUNT_TOTAL",
    "C2_COUNT_MEN+",
    "C3_COUNT_WOMEN+",
    "C10_RATE_TOTAL",
    "C11_RATE_MEN+",
    "C12_RATE_WOMEN+"
]

# Create relationship between characteristic and column
con.execute("""
    CREATE TABLE characteristic_columns (
        CENSUS_YEAR INTEGER,
        CHARACTERISTIC_ID INTEGER,
        column_id INTEGER
    );
""")

for i, column in enumerate(columns, start=1):
    con.execute(f"""
        INSERT INTO characteristic_columns
        SELECT DISTINCT
            CENSUS_YEAR,
            CHARACTERISTIC_ID,
            {i}
        FROM '{input_file}'
        WHERE "{column}" IS NOT NULL;
    """)

con.execute("""
    COPY column_values
    TO 'parquet_data/2021_columns.parquet'
""")

con.execute("""
    COPY characteristic_columns
    TO 'parquet_data/2021_characteristic_columns.parquet'
""")

# preprocess 2016 census data
input_file = 'temp_parquet_data/2016_raw_census_data.parquet'

con.execute(f"""
    COPY (
        SELECT
            CENSUS_YEAR,
            GEO_CODE,
            CHARACTERISTIC_ID,
            COUNT_TOTAL,
            COUNT_MALE,
            COUNT_FEMALE
        FROM '{input_file}'
    )
    TO 'parquet_data/2016_census_data.parquet'
    (FORMAT PARQUET, COMPRESSION ZSTD);
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
    TO 'parquet_data/2016_characteristics.parquet'
    (FORMAT PARQUET, COMPRESSION ZSTD)
""")

# Geography lookup table
con.execute(f"""
    COPY (
        SELECT DISTINCT
            CENSUS_YEAR,
            GEO_CODE,
            GEO_LEVEL,
            GEO_NAME
        FROM '{input_file}'
        ORDER BY GEO_CODE
    )
    TO 'parquet_data/2016_geographies.parquet'
    (FORMAT PARQUET, COMPRESSION ZSTD)
""")

# List of data columns
con.execute("""
    CREATE TABLE IF NOT EXISTS column_values (
        column_id INTEGER PRIMARY KEY,
        column_name VARCHAR
    );
""")

con.execute("""
    INSERT INTO column_values VALUES
        (7, 'COUNT_MALE'),
        (8, 'COUNT_FEMALE');     
""")

columns = [
    "COUNT_TOTAL",
    "COUNT_MALE",
    "COUNT_FEMALE",
]

# Create relationship between characteristic and column
for i, column in enumerate(columns, start=1):
    con.execute(f"""
        INSERT INTO characteristic_columns
        SELECT DISTINCT
            CENSUS_YEAR,
            CHARACTERISTIC_ID,
            {i}
        FROM '{input_file}'
        WHERE "{column}" IS NOT NULL;
    """)

con.execute("""
    COPY column_values
    TO 'parquet_data/2016_columns.parquet'
""")

con.execute("""
    COPY characteristic_columns
    TO 'parquet_data/2016_characteristic_columns.parquet'
""")

con.close()