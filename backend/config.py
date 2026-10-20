import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

PARQUET_DIR = BASE_DIR / "parquet_data"
TILES_DIR = BASE_DIR / "tiles_output"

NHS_DA_YEAR = 2010

CORS_ORIGINS = [
    origin.strip()
    for origin in os.getenv("CORS_ORIGINS", "").split(",")
    if origin.strip()
]

LOCALHOST_ORIGIN_REGEX = r"^https?://(localhost|127\.0\.0\.1)(:\d+)?$"

MAIN_TABLE = PARQUET_DIR / "2021_census_data.parquet"
GEO_TABLE = PARQUET_DIR / "2021_geographies.parquet"
