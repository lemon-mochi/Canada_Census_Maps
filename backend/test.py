import duckdb

con = duckdb.connect()

char_file = "parquet_data/2011_characteristics.parquet"

res = con.execute(f"""
    SELECT *
    FROM '{char_file}'
    WHERE CHARACTERISTIC_ID=105
""").fetchdf()

print(res)

input_file = "temp_parquet_data/2011_raw_census_data.parquet"

res = con.execute(f"""
    SELECT *
    FROM '{input_file}'
    WHERE GEO_CODE=10010732
""").fetchdf()

print(res)

con.close()