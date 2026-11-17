from functools import lru_cache
from pathlib import Path

import duckdb
from fastapi import HTTPException

from services.census_constants import *


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
            column_names = {column["column_name"] for column in columns}

            columns.append(
                {
                    "column_id": 4,
                    "column_name": "RATE_TOTAL",
                }
            )

            if "COUNT_MALE" in column_names:
                columns.append(
                    {
                        "column_id": 5,
                        "column_name": "RATE_MALE",
                    }
                )

            if "COUNT_FEMALE" in column_names:
                columns.append(
                    {
                        "column_id": 6,
                        "column_name": "RATE_FEMALE",
                    }
                )
        result.append(
            {
                "CHARACTERISTIC_ID": int(char_id),
                "CHARACTERISTIC_NAME": name.strip(),
                "level": indent_level(name),
                "columns": columns,
            }
        )

    return result
