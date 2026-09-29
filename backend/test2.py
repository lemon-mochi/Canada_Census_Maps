import duckdb

con = duckdb.connect()

input_file = 'temp_parquet_data/2011_raw_nhs_da.parquet'

res = con.execute(f"""
    SELECT *
    FROM '{input_file}'
    WHERE CHARACTERISTIC_ID=473
""").fetchdf()

print(res)

con.close()