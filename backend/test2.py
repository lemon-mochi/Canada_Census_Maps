import duckdb

con = duckdb.connect()

input_file = 'temp_parquet_data/2006_raw_census_data.parquet'

res = con.execute(f"""
    SELECT *
    FROM '{input_file}'
    WHERE (GEO_CODE='01' AND CHARACTERISTIC_ID=1)
""").fetchdf()

print(res)

con.close()