import duckdb

con = duckdb.connect()

input_file = "temp_parquet_data/2011_raw_nhs_da.parquet"

res = con.execute(f"""
    SELECT GEO_ID, TOTAL
    FROM '{input_file}'
""").fetchdf()

print(res)

con.close()