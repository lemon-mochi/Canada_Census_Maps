from pathlib import Path
# import requests
# import io
# import zipfile
import colour_data

import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import duckdb


app = FastAPI()
con = duckdb.connect()

main_table = 'parquet_data/2021_census_data.parquet'
geo_table = 'parquet_data/2021_geographies.parquet'
char_table = 'parquet_data/2021_characteristics.parquet'
col_table = 'parquet_data/2021_columns.parquet'
char_col_table = 'parquet_data/2021_characteristic_columns.parquet'

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent

print("BASE_DIR:", BASE_DIR)
print("Tiles directory:", BASE_DIR / "tiles_output")
print("Exists:", (BASE_DIR / "tiles_output").exists())
print("Files:", list((BASE_DIR / "tiles_output").glob("*")))

app.mount(
    "/tiles_output",
    StaticFiles(directory=BASE_DIR / "tiles_output"),
    name="tiles_output",
)


@app.get("/api/characteristics")
def get_characteristics(year: int):

    result = con.execute(f"""
        SELECT
            c.CHARACTERISTIC_ID,
            c.CHARACTERISTIC_NAME,
            cc.column_id,
            col.column_name
        FROM '{char_table}' AS c

        LEFT JOIN '{char_col_table}' AS cc
            ON c.CENSUS_YEAR = cc.CENSUS_YEAR
            AND c.CHARACTERISTIC_ID = cc.CHARACTERISTIC_ID

        LEFT JOIN '{col_table}' AS col
            ON cc.column_id = col.column_id

        WHERE c.CENSUS_YEAR = {year}

        ORDER BY c.CHARACTERISTIC_ID, cc.column_id
    """).fetchdf()

    characteristics = []

    for char_id, group in result.groupby(
        "CHARACTERISTIC_ID",
        sort=False
    ):
        first = group.iloc[0]

        columns = []

        for _, row in group.iterrows():
            if row["column_id"] is not None:
                columns.append({
                    "column_id": int(row["column_id"]),
                    "column_name": row["column_name"]
                })

        characteristics.append({
            "CHARACTERISTIC_ID": int(char_id),
            "CHARACTERISTIC_NAME": first["CHARACTERISTIC_NAME"],
            "columns": columns
        })

    return characteristics


@app.get("/api/population")
def get_population(geo_level: str, char_id: int):

    if (geo_level == 'Province'):
        result = con.execute(f"""
            SELECT m.DGUID, m.C1_COUNT_TOTAL
            FROM '{main_table}' AS m
            JOIN '{geo_table}' AS g ON m.DGUID = g.DGUID
            WHERE 
                (g.GEO_LEVEL = 'Province' OR g.GEO_LEVEL = 'Territory')
                AND m.CHARACTERISTIC_ID = {char_id}
        """).fetchdf()

    else:
        result = con.execute(f"""
            SELECT m.DGUID, m.C1_COUNT_TOTAL
            FROM '{main_table}' AS m
            JOIN '{geo_table}' AS g ON m.DGUID = g.DGUID
            WHERE 
                (g.GEO_LEVEL = '{geo_level}')
                AND m.CHARACTERISTIC_ID = {char_id}
        """).fetchdf()

    result_w_colours = colour_data.assign_colours(
        df=result,
        num_colours=3,
        equal_width=True,
        col='C1_COUNT_TOTAL'
    )

    return result_w_colours.to_dict(orient='records')

@app.get("/api/columns")
def get_columns(year: int, char_id: int):
    result = con.execute(f"""
        SELECT char_col.column_id
        FROM '{char_col_table}' as char_col
        JOIN '{col_table}' as col on col.column_id = char_col.column_id
        WHERE
            (char_col.CENSUS_YEAR = {year} AND char_col.CHARACTERISTIC_ID = {char_id})
    """).fetchdf()

    return result.to_dict(orient='records')
