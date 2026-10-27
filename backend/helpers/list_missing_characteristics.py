"""
-------------------------------
list_missing_characteristics.py
-------------------------------
This file lists the missing characteristic per geographic level.
To run,

python3 list_missing_characteristics.py

"""

# problem: sometimes, there are specific geographies where the value is
# N/A but there are still valid values in other geographies for the same
# geographic level. Look into this.

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

sample_geographies_2016 = {
    "Canada": "01",
    "Province/Territory": "60",
    "Census division": "1001",
    "Census subdivision": "1001519",
    "Dissemination area": "10010039",
    "Federal electoral district (2013 representation order)": "10001",
    "Aggregate dissemination area": "10010001",
}

sample_geographies_2011_06 = {
    "Canada": "01",
    "Province/Territory": "60",
    "Census division": "1001",
    "Census subdivision": "1001519",
    "Dissemination area": "10010039",
    "Census tract": "0010002.00",
    "Federal electoral district (2003 representation order)": "10001",
}

sample_geographies_2001 = {
    "Canada": "01",
    "Province/Territory": "10",
    "Census division": "1001",
    "Census subdivision": "1001101",
    "Dissemination area": "10010039",
    "Census tract": "0010002.00",
    "Federal electoral district (1996 representation order)": "10002",
}

sample_geographies_1996 = {
    "Canada": "00",
    "Province/Territory": "10",
    "Census division": "1001",
    "Census subdivision": "1001101",
    "Enumeration area": "10001002",
    "Census tract": "0010002.00",
    "Federal electoral district (1996 representation order)": "10002",
}

sample_geographies_1991 = {
    "Canada": "00",
    "Province/Territory": "10",
    "Census division": "1001",
    "Census subdivision": "1001101",
    "Enumeration area": "10001002",
    "Census tract": "0010002.00",
    "Federal electoral district (1996 representation order)": "10002",
}

sample_geographies_1986_81 = {
    "Canada": "00",
    "Province/Territory": "10",
    "Census division": "1001",
    "Census subdivision": "1001101",
    "Census tract": "0010002.00",
}


def get_missing_new(input_file, char_file, sample_geographies, f):
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
                )
                ORDER BY c.CHARACTERISTIC_ID;
            """
        ).df()

        print(res.to_string(), file=f)


def get_missing_old(input_file, char_file, sample_geographies, f):
    for geography in sample_geographies:
        print(geography, file=f)
        res = con.execute(
            f"""
                SELECT c.CHARACTERISTIC_ID, c.CHARACTERISTIC_NAME
                FROM '{input_file}' AS i
                LEFT JOIN '{char_file}' AS c
                ON c.CHARACTERISTIC_ID=i.CHARACTERISTIC_ID
                WHERE (
                    GEO_CODE='{sample_geographies[geography]}'
                    AND i.COUNT_TOTAL IS NULL
                )
                ORDER BY c.CHARACTERISTIC_ID;
            """
        ).df()

        print(res.to_string(), file=f)


with open("missing_characteristics.txt", "w") as f:
    input_file = "../parquet_data/2021_census_data.parquet"
    char_file = "../parquet_data/2021_characteristics.parquet"
    print("Census year: 2021", file=f)
    get_missing_new(input_file, char_file, sample_geographies_2021, f)

    input_file = "../parquet_data/2016_census_data.parquet"
    char_file = "../parquet_data/2016_characteristics.parquet"
    print("Census year: 2016", file=f)
    get_missing_old(input_file, char_file, sample_geographies_2016, f)

    input_file = "../parquet_data/2011_census_data.parquet"
    char_file = "../parquet_data/2011_characteristics.parquet"
    print("Census year: 2011", file=f)
    get_missing_old(input_file, char_file, sample_geographies_2011_06, f)

    input_file = "../parquet_data/2006_census_data.parquet"
    char_file = "../parquet_data/2006_characteristics.parquet"
    print("Census year: 2006", file=f)
    get_missing_old(input_file, char_file, sample_geographies_2011_06, f)

    input_file = "../parquet_data/2001_census_data.parquet"
    char_file = "../parquet_data/2001_characteristics.parquet"
    print("Census year: 2001", file=f)
    get_missing_old(input_file, char_file, sample_geographies_2001, f)

    input_file = "../parquet_data/1996_census_data.parquet"
    char_file = "../parquet_data/1996_characteristics.parquet"
    print("Census year: 1996", file=f)
    get_missing_old(input_file, char_file, sample_geographies_1996, f)

    input_file = "../parquet_data/1991_census_data.parquet"
    char_file = "../parquet_data/1991_characteristics.parquet"
    print("Census year: 1991", file=f)
    get_missing_old(input_file, char_file, sample_geographies_1991, f)

    input_file = "../parquet_data/1986_census_data.parquet"
    char_file = "../parquet_data/1986_characteristics.parquet"
    print("Census year: 1986", file=f)
    get_missing_old(input_file, char_file, sample_geographies_1986_81, f)

    input_file = "../parquet_data/1981_census_data.parquet"
    char_file = "../parquet_data/1981_characteristics.parquet"
    print("Census year: 1981", file=f)
    get_missing_old(input_file, char_file, sample_geographies_1986_81, f)
