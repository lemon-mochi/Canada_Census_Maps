import duckdb

con = duckdb.connect()

input_file = 'parquet_data/1996_census_data.parquet'

res = con.execute(f"""
    SELECT *
    FROM '{input_file}'
    WHERE GEO_CODE=10001014
""").fetchdf()

print(res)

con.close()