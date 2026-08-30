from pathlib import Path
import requests
import io
import zipfile

import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles


app = FastAPI()

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

@app.get("/debug")
def debug():
    tiles_dir = BASE_DIR / "tiles_output"

    return {
        "directory": str(tiles_dir),
        "exists": tiles_dir.exists(),
        "files": [f.name for f in tiles_dir.iterdir()] if tiles_dir.exists() else [],
    }

PRODUCT_ID = 98100001
STATCAN_API_URL = f"https://www150.statcan.gc.ca/t1/wds/rest/getFullTableDownloadCSV/{PRODUCT_ID}/en"

CACHED_POPULATION_DATA = None

@app.get("/api/province-population")
def get_province_population():
    global CACHED_POPULATION_DATA
    if CACHED_POPULATION_DATA is not None:
        return {"status": "success", "data": CACHED_POPULATION_DATA}

    # 1. Fetch dynamic download URL from StatCan
    res = requests.get(STATCAN_API_URL, headers={"User-Agent": "Mozilla/5.0"})
    data = res.json()

    if data.get("status") != "SUCCESS":
        return {"status": "error", "message": "Failed to fetch CSV from StatCan API"}

    # 2. Extract CSV into RAM
    zip_res = requests.get(data.get("object"))
    zip_file = zipfile.ZipFile(io.BytesIO(zip_res.content))
    csv_filename = [f for f in zip_file.namelist() if f.endswith(".csv") and not f.endswith("_MetaData.csv")][0]

    with zip_file.open(csv_filename) as f:
        population_column = (
            "Population and dwelling counts (11): Population, 2021 [1]"
        )        
        # Load necessary fields
        df = pd.read_csv(
            f,
            usecols=["GEO", "DGUID", population_column],
            low_memory=False
        )

        # Extract PRUID from the last two digits of DGUID
        df["PRUID"] = df["DGUID"].str[-2:]

        # Keep only the province id and 2021 population
        df = df[["PRUID", population_column]]

        # Remove rows where population isn't available
        df = df.dropna(subset=[population_column])

        return {
            "data": {
                row["PRUID"]: row[population_column]
                for _, row in df.iterrows()
            }
        }