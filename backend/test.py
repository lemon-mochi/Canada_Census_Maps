import duckdb

con = duckdb.connect()

main_table = 'parquet_data/2021_census_data.parquet'
geo_table = 'parquet_data/2021_geographies.parquet'

def get_population(char_id=1):

    result = con.execute(f"""
        SELECT m.DGUID, m.C1_COUNT_TOTAL
        FROM '{main_table}' AS m
        JOIN '{geo_table}' AS g ON m.DGUID = g.DGUID
        WHERE 
            (g.GEO_LEVEL = 'Province' OR g.GEO_LEVEL = 'Territory')
            AND m.CHARACTERISTIC_ID = {char_id}
    """).fetchdf()

    print(result)

    return result.to_json(orient='records')

def dguid_pr():
    result = con.execute(f"""
        SELECT DGUID, GEO_NAME
        FROM '{geo_table}'
        WHERE GEO_LEVEL = 'Province' or GEO_LEVEL = 'Territory'
    """).fetchdf()

    print(result)

    return result.to_json(orient='records')

# 1488 is for Median value of dwellings ($).
# I know it is also a hate symbol but that is just a coincidence.
print(get_population(char_id=1488))

dguid_pr()