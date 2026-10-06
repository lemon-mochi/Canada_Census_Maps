import duckdb

con = duckdb.connect()
input_file = 'parquet_data/1981_census_data.parquet'

print(con.execute(f"""
    SELECT *
    FROM '{input_file}'
    WHERE GEO_CODE='10'
        AND CHARACTERISTIC_ID=1
    ORDER BY CHARACTERISTIC_ID
""").df())

con.close()