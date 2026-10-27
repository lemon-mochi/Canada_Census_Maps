import duckdb

con = duckdb.connect()
input_file = "temp_parquet_data/2006_raw_census_data.parquet"

print(con.execute(f"""
    DESCRIBE SELECT * FROM '{input_file}'
""").fetchdf())

print(con.execute(f"""
    SELECT *
    FROM '{input_file}'
    WHERE GEO_CODE IS NULL
       OR CHARACTERISTIC_ID IS NULL
    LIMIT 10
""").fetchdf())

print(con.execute(f"""
    SELECT GEO_CODE, CHARACTERISTIC_ID, COUNT(*) AS n
    FROM '{input_file}'
    GROUP BY GEO_CODE, CHARACTERISTIC_ID
    HAVING COUNT(*) > 1
    LIMIT 10
""").fetchdf())
