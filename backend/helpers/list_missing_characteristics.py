"""
-------------------------------
list_missing_characteristics.py
-------------------------------
This file lists the missing characteristic per geographic level.
To run,

python3 list_missing_characteristics.py

"""

import duckdb

con = duckdb.connect()

sample_geographies_2021 = {
    "Canada": "2021A000011124",
    "Province/Territory": "2021A000260",
    "Census division": "2021A00036001",
    "Census subdivision": "2021A00056001003",
    "Dissemination area": "2021S051260010250",
    "Aggregate dissemination area": "2021S051610010001",
    "Federal electoral district (2013 representation order)": "2013A000410001",
    "Federal electoral district (2023 representation order)": "2023A000410001",
}

def get_missing(input_file, char_file, sample_geographies, f):
    for geography in sample_geographies:
            print(geography, file=f)
            res = con.execute(
                f"""
                SELECT c.CHARACTERISTIC_ID, c.CHARACTERISTIC_NAME
                FROM '{input_file}' AS i
                LEFT JOIN '{char_file}' AS c
                ON c.CHARACTERISTIC_ID=i.CHARACTERISTIC_ID
                WHERE (
                    DGUID='{sample_geographies[geography]}'
                    AND i.C1_COUNT_TOTAL IS NULL
                );
            """
            ).df()

            print(res, file=f)

with open("missing_characteristics.txt", "w") as f:
    input_file = "../parquet_data/2021_census_data.parquet"
    char_file = "../parquet_data/2021_characteristics.parquet"
    print("Census year: 2021", file=f)
    get_missing(input_file, char_file, sample_geographies_2021, f)
