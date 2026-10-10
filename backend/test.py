import duckdb

con = duckdb.connect()
input_file = 'parquet_data/2021_census_data.parquet'

print(con.execute(f"""
    SELECT DGUID, CHARACTERISTIC_ID, C1_COUNT_TOTAL
    FROM '{input_file}'
    WHERE DGUID='2023A000459017'
    ORDER BY CHARACTERISTIC_ID
""").df())

con.close()