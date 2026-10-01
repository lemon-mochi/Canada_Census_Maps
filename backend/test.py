import duckdb

con = duckdb.connect()
input_file = 'parquet_data/2021_census_data.parquet'

print(con.execute(f"""
    SELECT *
    FROM '{input_file}'
    WHERE DGUID='2021A000011124'
    ORDER BY CHARACTERISTIC_ID
""").df())

con.close()