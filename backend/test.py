import duckdb

con = duckdb.connect()
input_file = "parquet_data/2006_census_data.parquet"
char_file = "parquet_data/2006_characteristics.parquet"

print(
    con.execute(
        f"""
    SELECT *
    FROM '{input_file}' AS i
    LEFT JOIN '{char_file}' AS c
    ON c.CHARACTERISTIC_ID=i.CHARACTERISTIC_ID
    WHERE (
        i.GEO_CODE='5941'
        AND i.CHARACTERISTIC_ID=11
    );
"""
    ).df()
)
