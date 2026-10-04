import logging
import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Literal, Optional

import duckdb
from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

import colour_data

logger = logging.getLogger("census_api")
logging.basicConfig(level=logging.INFO)

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
PARQUET_DIR = BASE_DIR / "parquet_data"
TILES_DIR = BASE_DIR / "tiles_output"

# The frontend sends 2010 to mean "2011 NHS dissemination-area data".
NHS_DA_YEAR = 2010

# Extra production origins, comma-separated, e.g. "https://example.com".
# Any localhost / 127.0.0.1 port is always allowed so dev servers
# (Vite 5173, Next 3000, etc.) work without configuration.
CORS_ORIGINS = [o.strip() for o in os.getenv("CORS_ORIGINS", "").split(",") if o.strip()]
LOCALHOST_ORIGIN_REGEX = r"^https?://(localhost|127\.0\.0\.1)(:\d+)?$"

MAIN_TABLE = PARQUET_DIR / "2021_census_data.parquet"
GEO_TABLE = PARQUET_DIR / "2021_geographies.parquet"

GeoLevel = Literal[
    "Province",
    "Census division",
    "Census subdivision",
    "Federal electoral district (2023 Representation Order)",
    "Federal electoral district (2013 Representation Order)",
    "Census tract",
    "Federal electoral district (1987 Representation Order)",
    "Federal electoral district (1996 Representation Order)",
    "Federal electoral district (2003 Representation Order)",
    "Federal electoral district (2013 Representation Order)",
    "Federal electoral district (2023 Representation Order)",
    "Aggregate dissemination area",
    "Dissemination area",
]

# Years before 2011 (and the 2011 NHS DA data) only have a total count and a
# total rate, so there is no per-year columns table for them.
LEGACY_COLUMNS = [
    {"column_id": 1, "column_name": "COUNT_TOTAL"},
    {"column_id": 4, "column_name": "RATE_TOTAL"},
]

# 2021 stores counts and rates directly.
COLUMNS_2021 = {
    1: "C1_COUNT_TOTAL",
    2: "C2_COUNT_MEN+",
    3: "C3_COUNT_WOMEN+",
    4: "C10_RATE_TOTAL",
    5: "C11_RATE_MEN+",
    6: "C12_RATE_WOMEN+",
}

# 2011 / 2016 store counts only; rates are computed against this row.
COUNT_COLUMNS_2011_2016 = {1: "COUNT_TOTAL", 2: "COUNT_MALE", 3: "COUNT_FEMALE"}
RATE_NUMERATORS_2011_2016 = {4: "COUNT_TOTAL", 5: "COUNT_MALE", 6: "COUNT_FEMALE"}
TOTAL_POPULATION_CHAR_ID_2011_2016 = 8

# ---------------------------------------------------------------------------
# App setup
# ---------------------------------------------------------------------------

app = FastAPI()
con = duckdb.connect()

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_origin_regex=LOCALHOST_ORIGIN_REGEX,
    allow_methods=["GET"],
    allow_headers=["*"],
)

if TILES_DIR.is_dir():
    app.mount("/tiles_output", StaticFiles(directory=TILES_DIR), name="tiles_output")
else:
    logger.warning("Tiles directory not found, not mounting: %s", TILES_DIR)


def get_db():
    """One DuckDB cursor per request; a single connection isn't thread-safe."""
    cursor = con.cursor()
    try:
        yield cursor
    finally:
        cursor.close()


# ---------------------------------------------------------------------------
# Response models
# ---------------------------------------------------------------------------


class Column(BaseModel):
    column_id: int
    column_name: Optional[str] = None


class Characteristic(BaseModel):
    CHARACTERISTIC_ID: int
    CHARACTERISTIC_NAME: str
    level: int  # nesting depth in the characteristic hierarchy (0 = top)
    columns: list[Column]


class PopulationValue(BaseModel):
    census_year: int
    geo_code: str
    characteristic_id: int
    value: Optional[float]

class Tiles(BaseModel):
    census_year: int
    geo_level: str
    url: str
    source_layer: str

# ---------------------------------------------------------------------------
# File helpers
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class YearFiles:
    data: Path
    chars: Path
    char_cols: Path
    cols: Path


def year_files(year: int) -> YearFiles:
    """The only place that knows how a census year maps to parquet files."""
    if year == NHS_DA_YEAR:
        data = PARQUET_DIR / "2011_nhs_da_data.parquet"
        chars = PARQUET_DIR / "2011_nhs_da_characteristics.parquet"
    else:
        data = PARQUET_DIR / f"{year}_census_data.parquet"
        chars = PARQUET_DIR / f"{year}_characteristics.parquet"

    return YearFiles(
        data=data,
        chars=chars,
        char_cols=PARQUET_DIR / f"{year}_characteristic_columns.parquet",
        cols=PARQUET_DIR / f"{year}_columns.parquet",
    )


def require(path: Path, detail: str) -> None:
    if not path.exists():
        raise HTTPException(status_code=404, detail=detail)


def indent_level(name: str) -> int:
    """Hierarchy depth, encoded in the source data as two leading spaces per level."""
    return (len(name) - len(name.lstrip(" "))) // 2


# ---------------------------------------------------------------------------
# /api/characteristics
# ---------------------------------------------------------------------------


@lru_cache(maxsize=32)
def load_characteristics(year: int) -> list[dict]:
    """Parquet files are static, so the result is cached per year.

    HTTPExceptions are not cached (lru_cache only stores returned values).
    """
    files = year_files(year)
    require(files.chars, f"Invalid census year: {year}")

    db = con.cursor()
    try:
        if year >= 2011:
            require(
                files.char_cols,
                f"Characteristic columns not found for census year: {year}",
            )
            require(files.cols, f"Column information not found for census year: {year}")

            rows = db.execute(
                """
                SELECT
                    c.CHARACTERISTIC_ID,
                    c.CHARACTERISTIC_NAME,
                    list(
                        {'column_id': col.column_id, 'column_name': col.column_name}
                        ORDER BY cc.column_id
                    ) FILTER (WHERE cc.column_id IS NOT NULL) AS columns
                FROM read_parquet(?) AS c
                LEFT JOIN read_parquet(?) AS cc
                    ON c.CHARACTERISTIC_ID = cc.CHARACTERISTIC_ID
                LEFT JOIN read_parquet(?) AS col
                    ON cc.column_id = col.column_id
                GROUP BY c.CHARACTERISTIC_ID, c.CHARACTERISTIC_NAME
                ORDER BY c.CHARACTERISTIC_ID
                """,
                [str(files.chars), str(files.char_cols), str(files.cols)],
            ).fetchall()
        else:
            rows = [
                (char_id, name, LEGACY_COLUMNS)
                for char_id, name in db.execute(
                    """
                    SELECT CHARACTERISTIC_ID, CHARACTERISTIC_NAME
                    FROM read_parquet(?)
                    ORDER BY CHARACTERISTIC_ID
                    """,
                    [str(files.chars)],
                ).fetchall()
            ]
    finally:
        db.close()

    result = []

    for char_id, name, columns in rows:
        columns = columns or []

        if year in (2011, 2016):
            columns = columns + [
                {"column_id": 4, "column_name": "RATE_TOTAL"},
                {"column_id": 5, "column_name": "RATE_MALE"},
                {"column_id": 6, "column_name": "RATE_FEMALE"},
            ]

        result.append(
            {
                "CHARACTERISTIC_ID": int(char_id),
                "CHARACTERISTIC_NAME": name.strip(),
                "level": indent_level(name),
                "columns": columns,
            }
        )

    return result


@app.get("/api/characteristics", response_model=list[Characteristic])
def get_characteristics(census_year: int):
    return load_characteristics(census_year)


# ---------------------------------------------------------------------------
# /api/population  (choropleth colours for a geographic level)
# ---------------------------------------------------------------------------


@app.get("/api/population")
def get_population(geo_level: GeoLevel, char_id: int, db=Depends(get_db)):
    levels = ("Province", "Territory") if geo_level == "Province" else (geo_level,)
    placeholders = ",".join("?" * len(levels))

    result = db.execute(
        f"""
        SELECT m.DGUID, m.C1_COUNT_TOTAL
        FROM read_parquet(?) AS m
        JOIN read_parquet(?) AS g ON m.DGUID = g.DGUID
        WHERE g.GEO_LEVEL IN ({placeholders})
          AND m.CHARACTERISTIC_ID = ?
        """,
        [str(MAIN_TABLE), str(GEO_TABLE), *levels, char_id],
    ).fetchdf()

    coloured = colour_data.assign_colours(
        df=result,
        num_colours=3,
        equal_width=True,
        col="C1_COUNT_TOTAL",
    )
    return coloured.to_dict(orient="records")


# ---------------------------------------------------------------------------
# /api/columns
# ---------------------------------------------------------------------------


@app.get("/api/columns")
def get_columns(census_year: int, char_id: int):
    """Column ids available for one characteristic in one census year."""
    for characteristic in load_characteristics(census_year):
        if characteristic["CHARACTERISTIC_ID"] == char_id:
            return [{"column_id": c["column_id"]} for c in characteristic["columns"]]

    raise HTTPException(status_code=404, detail="Characteristic not found")


# ---------------------------------------------------------------------------
# /api/specific_population
# ---------------------------------------------------------------------------


def read_value(db, file: Path, geo_column: str, geo_code: str, char_id: int, column: str):
    """Return (found, value). Column and geo_column come from the constants above,
    never from user input, so interpolating them is safe."""
    row = db.execute(
        f"""
        SELECT "{column}"
        FROM read_parquet(?)
        WHERE "{geo_column}" = ?
          AND CHARACTERISTIC_ID = ?
        """,
        [str(file), geo_code, char_id],
    ).fetchone()
    return (row is not None), (row[0] if row else None)


def read_required(db, *args) -> float:
    found, value = read_value(db, *args)
    if not found:
        raise HTTPException(status_code=404, detail="Population data not found")
    return value


def safe_rate(numerator, denominator) -> Optional[float]:
    if numerator is None or denominator in (None, 0):
        return None
    return numerator / denominator


def legacy_value(db, year, file, geo_code, char_id, value):
    """1981-2006 and 2011 NHS DA: total count (1) and total rate (4) only."""
    if value not in (1, 4):
        raise HTTPException(status_code=400, detail="Invalid value")

    count = read_required(db, file, "GEO_CODE", geo_code, char_id, "COUNT_TOTAL")
    if value == 1:
        return count

    total_char_id = 1 if year == NHS_DA_YEAR else 2
    _, total = read_value(db, file, "GEO_CODE", geo_code, total_char_id, "COUNT_TOTAL")
    return safe_rate(count, total)


def two_sex_value(db, file, geo_code, char_id, value):
    """2011 and 2016: total/male/female counts, rates derived from char 8."""
    if value in COUNT_COLUMNS_2011_2016:
        column = COUNT_COLUMNS_2011_2016[value]
        return read_required(db, file, "GEO_CODE", geo_code, char_id, column)

    column = RATE_NUMERATORS_2011_2016[value]
    numerator = read_required(db, file, "GEO_CODE", geo_code, char_id, column)
    _, denominator = read_value(
        db, file, "GEO_CODE", geo_code, TOTAL_POPULATION_CHAR_ID_2011_2016, column
    )
    return safe_rate(numerator, denominator)


def stored_value(db, file, geo_code, char_id, value):
    """2021: counts and rates are already stored."""
    if value not in COLUMNS_2021:
        raise HTTPException(status_code=400, detail="Invalid value")
    return read_required(db, file, "DGUID", geo_code, char_id, COLUMNS_2021[value])


@app.get("/api/specific_population", response_model=PopulationValue)
def get_specific_population(
    census_year: int,
    geo_code: str,
    char_id: int,
    value: int = Query(..., ge=1, le=6),
    db=Depends(get_db),
):
    file = year_files(census_year).data
    require(file, f"Invalid census year: {census_year}")

    if census_year <= NHS_DA_YEAR:
        result = legacy_value(db, census_year, file, geo_code, char_id, value)
    elif census_year in (2011, 2016):
        result = two_sex_value(db, file, geo_code, char_id, value)
    elif census_year == 2021:
        result = stored_value(db, file, geo_code, char_id, value)
    else:
        raise HTTPException(status_code=400, detail="Unsupported census year")

    return PopulationValue(
        census_year=census_year,
        geo_code=geo_code,
        characteristic_id=char_id,
        value=result,
    )

def vector_tile_path(census_year: int, geo_level: str) -> Path:
    if census_year == 1981:
        if geo_level == "Province":
            return TILES_DIR / "prov1981_poly_geojson.pmtiles"
        elif geo_level == "Census division":
            return TILES_DIR / "cd_dr1981_poly_geojson.pmtiles"
        elif geo_level == "Census subdivision":
            return TILES_DIR / "csd1981_poly_geojson.pmtiles"
        elif geo_level == "Census tract":
            return TILES_DIR / "ct_1981_orig_CBF.pmtiles"

    elif census_year == 1986:
        if geo_level == "Province":
            return TILES_DIR / "can86prov_geojson.pmtiles"
        elif geo_level == "Census division":
            return TILES_DIR / "cd86_geojson.pmtiles"
        elif geo_level == "Census subdivision":
            return TILES_DIR / "csd86_geojson.pmtiles"
        elif geo_level == "Census tract":
            return TILES_DIR / "1986_ct.pmtiles" 

    elif census_year == 1991:
        if geo_level == "Province":
            return TILES_DIR / "l91prv_geojson.pmtiles"
        elif geo_level == "Census division":
            return TILES_DIR / "l91cd_geojson.pmtiles"
        elif geo_level == "Census subdivision":
            return TILES_DIR / "l91csd_geojson.pmtiles"
        elif geo_level == "Federal electoral district (1987 Representation Order)":
            return TILES_DIR / "l91fed_geojson.pmtiles"
        elif geo_level == "Census tract":
            return TILES_DIR / "1991_ct.pmtiles"

    elif census_year == 1996:
        if geo_level == "Province":
            return TILES_DIR / "GPRE000A_geojson.pmtiles"
        elif geo_level == "Census division":
            return TILES_DIR / "GCD_000A_geojson.pmtiles"
        elif geo_level == "Census subdivision":
            return TILES_DIR / "GCSD000A_geojson.pmtiles"
        elif geo_level == "Census tract":
            return TILES_DIR / "GCT_000A_geojson.pmtiles"
        elif geo_level == "Federal electoral district (1996 Representation Order)":
            return TILES_DIR / "GFED000A_geojson.pmtiles"
        elif geo_level == "Enumeration area":
            return TILES_DIR / "GEA_000A_geojson.pmtiles"

    elif census_year == 2001:
        if geo_level == "Province":
            return TILES_DIR / "gpr_000b02m_e_geojson.pmtiles"
        elif geo_level == "Census division":
            return TILES_DIR / "gcd_000b02m_e_geojson.pmtiles"
        elif geo_level == "Census subdivision":
            return TILES_DIR / "gcsd000b02m_e_geojson.pmtiles"
        elif geo_level == "Census tract":
            return TILES_DIR / "gct_000b02m_e_geojson.pmtiles"
        elif geo_level == "Federal electoral district (1996 Representation Order)":
            return TILES_DIR / "gfed000b02m_e_geojson.pmtiles"
        elif geo_level == "Dissemination area":
            return TILES_DIR / "gda_000b02m_e_geojson.pmtiles"

    elif census_year == 2006:
        if geo_level == "Province":
            return TILES_DIR / "gpr_000b06a_e.pmtiles"
        elif geo_level == "Census division":
            return TILES_DIR / "gcd_000b06a_e.pmtiles"
        elif geo_level == "Census subdivision":
            return TILES_DIR / "gcsd000b06a_e.pmtiles"
        elif geo_level == "Federal electoral district (2003 Representation Order)":
            return TILES_DIR / "gfed000b06a_e.pmtiles"
        elif geo_level == "Census tract":
            return TILES_DIR / "gct_000b06a_e.pmtiles"
        elif geo_level == "Dissemination area":
            return TILES_DIR / "gda_000b06a_e.pmtiles"

    elif census_year == 2010:
        return TILES_DIR / "gda_000b11a_e.pmtiles"

    elif census_year == 2011:
        if geo_level == "Province":
            return TILES_DIR / "gpr_000b11a_e.pmtiles"
        elif geo_level == "Census division":
            return TILES_DIR / "gcd_000b11a_e.pmtiles"
        elif geo_level == "Census subdivision":
            return TILES_DIR / "gcsd000b11a_e.pmtiles"
        elif geo_level == "Federal electoral district (2003 Representation Order)":
            return TILES_DIR / "gfed000b11a_e.pmtiles"
        elif geo_level == "Census tract":
            return TILES_DIR / "gct_000b11a_e.pmtiles"
        elif geo_level == "Dissemination area":
            return TILES_DIR / "gda_000b11a_e.pmtiles"

    elif census_year == 2016:
        if geo_level == "Province":
            return TILES_DIR / "lpr_000b16a_e.pmtiles"
        elif geo_level == "Census division":
            return TILES_DIR / "lcd_000b16a_e.pmtiles"
        elif geo_level == "Census subdivision":
            return TILES_DIR / "lcsd000b16a_e.pmtiles"
        elif geo_level == "Federal electoral district (2013 Representation Order)":
            return TILES_DIR / "lfed000b16a_e.pmtiles"
        elif geo_level == "Aggregate dissemination area":
            return TILES_DIR / "lada000b16a_e.pmtiles"
        elif geo_level == "Dissemination area":
            return TILES_DIR / "lda_000b16a_e.pmtiles"

    elif census_year == 2021:
        if geo_level == "Province":
            return TILES_DIR / "lpr_000b21a_e.pmtiles"
        elif geo_level == "Census division":
            return TILES_DIR / "lcd_000b21a_e.pmtiles"
        elif geo_level == "Census subdivision":
            return TILES_DIR / "lcsd000b21a_e.pmtiles"
        elif geo_level == "Federal electoral district (2013 Representation Order)":
            return TILES_DIR / "lfed000b21a_e.pmtiles"
        elif geo_level == "Federal electoral district (2023 Representation Order)":
            return TILES_DIR / "FED_CA_2023_EN.pmtiles"
        elif geo_level == "Aggregate dissemination area":
            return TILES_DIR / "lada000b21a_e.pmtiles"
        elif geo_level == "Dissemination area":
            return TILES_DIR / "lda_000b21a_e.pmtiles"

    raise HTTPException(
        status_code=404,
        detail=f"No vector tiles available for {census_year} / {geo_level}",
    )

@app.get("/api/vector_tiles", response_model=Tiles)
def get_vector_tiles(census_year: int, geo_level: GeoLevel):
    path = vector_tile_path(census_year, geo_level)

    if not path.is_file():
        raise HTTPException(
            status_code=404,
            detail=f"Vector tile file not found: {path.name}",
        )

    return Tiles(
        census_year=census_year,
        geo_level=geo_level,
        url=f"/tiles_output/{path.name}",
        source_layer=path.stem,
    )
