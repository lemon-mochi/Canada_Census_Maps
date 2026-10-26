import duckdb
import pandas as pd

con = duckdb.connect()


def print_schema(input_file, f):
    res = con.execute(
        f"""
        DESCRIBE '{input_file}'
    """
    ).df()

    print(res, file=f)


with open("census_data_descriptions.txt", "w") as f:
    years = ["1981", "1986", "1991", "1996", "2001", "2006", "2011", "2016", "2021"]
    for year in years:
        print(year, file=f)
        input_file = f"../parquet_data/{year}_census_data.parquet"
        print_schema(input_file, f)

    # 2011 NHS DA is a special case
    print("2011 NHS DA", file=f)
    input_file = "../parquet_data/2011_nhs_da_data.parquet"
    print_schema(input_file, f)

con.close()
