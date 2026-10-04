from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Optional

import duckdb
from fastapi import HTTPException

from config import NHS_DA_YEAR, PARQUET_DIR


LEGACY_COLUMNS = [
    {"column_id": 1, "column_name": "COUNT_TOTAL"},
    {"column_id": 4, "column_name": "RATE_TOTAL"},
]

COLUMNS_2021 = {
    1: "C1_COUNT_TOTAL",
    2: "C2_COUNT_MEN+",
    3: "C3_COUNT_WOMEN+",
    4: "C10_RATE_TOTAL",
    5: "C11_RATE_MEN+",
    6: "C12_RATE_WOMEN+",
}

COUNT_COLUMNS_2011_2016 = {
    1: "COUNT_TOTAL",
    2: "COUNT_MALE",
    3: "COUNT_FEMALE",
}

RATE_NUMERATORS_2011_2016 = {
    4: "COUNT_TOTAL",
    5: "COUNT_MALE",
    6: "COUNT_FEMALE",
}

TOTAL_POPULATION_CHAR_ID_2011_2016 = 8


@dataclass(frozen=True)
class YearFiles:
    data: Path
    chars: Path
    char_cols: Path
    cols: Path


def year_files(year: int) -> YearFiles:
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
    return (len(name) - len(name.lstrip(" "))) // 2


@lru_cache(maxsize=32)
def load_characteristics(year: int) -> list[dict]:
    files = year_files(year)

    require(files.chars, f"Invalid census year: {year}")

    db = duckdb.connect()

    try:
        if year >= 2011:
            require(
                files.char_cols,
                f"Characteristic columns not found for census year: {year}",
            )
            require(
                files.cols,
                f"Column information not found for census year: {year}",
            )

            rows = db.execute(
                """
                SELECT
                    c.CHARACTERISTIC_ID,
                    c.CHARACTERISTIC_NAME,
                    list(
                        {
                            'column_id': col.column_id,
                            'column_name': col.column_name
                        }
                        ORDER BY cc.column_id
                    ) FILTER (WHERE cc.column_id IS NOT NULL) AS columns
                FROM read_parquet(?) AS c
                LEFT JOIN read_parquet(?) AS cc
                    ON c.CHARACTERISTIC_ID = cc.CHARACTERISTIC_ID
                LEFT JOIN read_parquet(?) AS col
                    ON cc.column_id = col.column_id
                GROUP BY
                    c.CHARACTERISTIC_ID,
                    c.CHARACTERISTIC_NAME
                ORDER BY c.CHARACTERISTIC_ID
                """,
                [
                    str(files.chars),
                    str(files.char_cols),
                    str(files.cols),
                ],
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