import duckdb

con = duckdb.connect()
input_file = 'parquet_data/1996_geographies.parquet'

print(con.execute(f"""
    SELECT *
    FROM '{input_file}'
    WHERE CTUID='9330243.02'
""").df())

con.close()