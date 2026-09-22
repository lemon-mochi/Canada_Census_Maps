import duckdb

con = duckdb.connect()

input_file = 'temp_parquet_data/2006_raw_census_data.parquet'

res = con.execute(f"""
    DESCRIBE '{input_file}'
""").fetchdf()

print(res)

con.close()