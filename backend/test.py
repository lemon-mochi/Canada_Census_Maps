import duckdb

con = duckdb.connect()

result = con.execute("""
    SELECT DGUID, C1_COUNT_TOTAL
    FROM 'parquet_data/2021_census_data.parquet'
    WHERE 
        (GEO_LEVEL='Province' OR GEO_LEVEL='Territory')
        AND CHARACTERISTIC_ID=1
""").fetchdf()

print(result)