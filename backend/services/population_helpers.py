from pathlib import Path
from fastapi import HTTPException
from typing import Optional

from services.census_constants import *


def read_value(
    db,
    file: Path,
    geo_column: str,
    geo_code: str,
    char_id: int,
    column: str,
):
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
        raise HTTPException(
            status_code=404,
            detail="Population data not found",
        )

    return value


def safe_rate(numerator, denominator) -> Optional[float]:
    if numerator is None or denominator in (None, 0):
        return None

    return numerator / denominator


def legacy_value(db, year, file, geo_code, char_id, value):
    if value not in (1, 4):
        raise HTTPException(status_code=400, detail="Invalid value")

    count = read_required(
        db,
        file,
        "GEO_CODE",
        geo_code,
        char_id,
        "COUNT_TOTAL",
    )

    if value == 1:
        return count

    total_char_id = 1 if year == NHS_DA_YEAR else 2

    _, total = read_value(
        db,
        file,
        "GEO_CODE",
        geo_code,
        total_char_id,
        "COUNT_TOTAL",
    )

    return safe_rate(count, total)


def two_sex_value(db, file, geo_code, char_id, value):
    if value in COUNT_COLUMNS_2011_2016:
        column = COUNT_COLUMNS_2011_2016[value]

        return read_required(
            db,
            file,
            "GEO_CODE",
            geo_code,
            char_id,
            column,
        )

    column = RATE_NUMERATORS_2011_2016[value]

    numerator = read_required(
        db,
        file,
        "GEO_CODE",
        geo_code,
        char_id,
        column,
    )

    _, denominator = read_value(
        db,
        file,
        "GEO_CODE",
        geo_code,
        TOTAL_POPULATION_CHAR_ID_2011_2016,
        column,
    )

    return safe_rate(numerator, denominator)


def stored_value(db, file, geo_code, char_id, value):
    if value not in COLUMNS_2021:
        raise HTTPException(status_code=400, detail="Invalid value")

    return read_required(
        db,
        file,
        "DGUID",
        geo_code,
        char_id,
        COLUMNS_2021[value],
    )


def read_values(
    db,
    file: Path,
    geo_column: str,
    geo_codes: list[str],
    char_id: int,
    column: str,
):
    if not geo_codes:
        return {}

    values = {str(geo_code): None for geo_code in geo_codes}

    rows = db.execute(
        f"""
        SELECT "{geo_column}", "{column}"
        FROM read_parquet(?)
        WHERE "{geo_column}" IN (
            SELECT UNNEST(?)
        )
          AND CHARACTERISTIC_ID = ?
        """,
        [str(file), geo_codes, char_id],
    ).fetchall()

    values.update({str(geo_code): value for geo_code, value in rows})

    return values
