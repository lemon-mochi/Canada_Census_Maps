import duckdb

con = duckdb.connect()
input_file = 'parquet_data/1991_census_data.parquet'

print(con.execute(f"""
    SELECT *
    FROM '{input_file}'
    WHERE GEO_CODE='9330250.00'
    ORDER BY CHARACTERISTIC_ID
""").df())

con.close()