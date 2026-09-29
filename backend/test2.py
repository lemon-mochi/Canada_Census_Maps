import duckdb

con = duckdb.connect()

input_file = 'temp_parquet_data/1986_raw_census_data.parquet'

res = con.execute(f"""
    SELECT *
    FROM '{input_file}'
    WHERE (GEO_CODE='59' AND CHARACTERISTIC_ID=427)
    ORDER BY CHARACTERISTIC_ID
""").fetchdf()

print(res)

con.close()