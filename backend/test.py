import duckdb

con = duckdb.connect()
input_file = 'parquet_data/1986_census_data.parquet'

print(con.execute(f"""
    SELECT *
    FROM '{input_file}'
    WHERE GEO_CODE='9330036.01'
        AND CHARACTERISTIC_ID=173
""").df())

con.close()