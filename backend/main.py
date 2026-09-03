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

@app.get("/api/population")
def get_population(geo_level: str, char_id: int):

    print(geo_level)
    print(char_id)

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
