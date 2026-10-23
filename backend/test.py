import duckdb

con = duckdb.connect()
input_file = 'parquet_data/1976_census_data.parquet'

print(con.execute(f"""
    SELECT *
    FROM '{input_file}'
    WHERE GEO_CODE='00'
""").df())