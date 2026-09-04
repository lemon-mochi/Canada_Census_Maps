from pathlib import Path
# import requests
# import io
# import zipfile

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
def get_characteristics():
    result = con.execute(f"""
        SELECT CHARACTERISTIC_ID, CHARACTERISTIC_NAME
        FROM '{char_table}'
    """).fetchdf()

    return result.to_dict(orient='records')


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

    return result.to_dict(orient='records')

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
