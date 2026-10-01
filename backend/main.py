from pathlib import Path
# import requests
# import io
# import zipfile
import colour_data

import pandas as pd
from fastapi import FastAPI, HTTPException
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

@app.get("/api/specific_population")
def get_specific_population(
    census_year: int,
    geo_code: str,
    char_id: int,
    value: int
):
    file = f"parquet_data/{census_year}_census_data.parquet"

    geo_column = "DGUID" if census_year == 2021 else "GEO_CODE"

    # 1981-2006: only total count and total rate
    if census_year <= 2006:
        if value not in (1, 4):
            raise HTTPException(status_code=400, detail="Invalid value")

        count_query = """
            SELECT COUNT_TOTAL
            FROM read_parquet(?)
            WHERE (GEO_CODE = ?
              AND CHARACTERISTIC_ID = ?
            )
        """

        result = con.execute(
            count_query,
            [file, geo_code, char_id]
        ).fetchone()

        if result is None:
            raise HTTPException(
                status_code=404,
                detail="Population data not found"
            )

        count = result[0]

        # value=1 -> count
        if value == 1:
            return {
                "census_year": census_year,
                "geo_code": geo_code,
                "characteristic_id": char_id,
                "value": count
            }

        # value=4 -> rate
        total_result = con.execute(
            """
            SELECT COUNT_TOTAL
            FROM read_parquet(?)
            WHERE GEO_CODE = ?
              AND CHARACTERISTIC_ID = 2
            """,
            [file, geo_code]
        ).fetchone()

        if total_result is None or total_result[0] in (None, 0):
            rate = None
        else:
            rate = count / total_result[0]

        return {
            "census_year": census_year,
            "geo_code": geo_code,
            "characteristic_id": char_id,
            "value": rate
        }

    # 2011 and 2016: total/male/female counts and rates
    elif census_year in (2011, 2016):
        if value not in (1, 2, 3, 4, 5, 6):
            raise HTTPException(status_code=400, detail="Invalid value")

        columns = {
            1: "COUNT_TOTAL",
            2: "COUNT_MALE",
            3: "COUNT_FEMALE"
        }

        # Counts
        if value in (1, 2, 3):
            column = columns[value]

            result = con.execute(
                f"""
                SELECT "{column}"
                FROM read_parquet(?)
                WHERE "{geo_column}" = ?
                  AND CHARACTERISTIC_ID = ?
                """,
                [file, geo_code, char_id]
            ).fetchone()

            print("result: ", result)

            if result is None:
                raise HTTPException(
                    status_code=404,
                    detail="Population data not found"
                )

            return {
                "census_year": census_year,
                "geo_code": geo_code,
                "characteristic_id": char_id,
                "value": result[0]
            }

        # Rates use CHARACTERISTIC_ID=8 as the total population row.
        numerator_columns = {
            4: "COUNT_TOTAL",
            5: "COUNT_MALE",
            6: "COUNT_FEMALE"
        }

        numerator_column = numerator_columns[value]

        numerator = con.execute(
            f"""
            SELECT "{numerator_column}"
            FROM read_parquet(?)
            WHERE "{geo_column}" = ?
              AND CHARACTERISTIC_ID = ?
            """,
            [file, geo_code, char_id]
        ).fetchone()

        if numerator is None:
            raise HTTPException(
                status_code=404,
                detail="Population data not found"
            )

        denominator = con.execute(
            f"""
            SELECT "{numerator_column}"
            FROM read_parquet(?)
            WHERE "{geo_column}" = ?
              AND CHARACTERISTIC_ID = 8
            """,
            [file, geo_code]
        ).fetchone()

        if denominator is None or denominator[0] in (None, 0):
            rate = None
        else:
            rate = numerator[0] / denominator[0]

        return {
            "census_year": census_year,
            "geo_code": geo_code,
            "characteristic_id": char_id,
            "value": rate
        }

    # 2021: counts and rates are already stored.
    elif census_year == 2021:
        columns = {
            1: "C1_COUNT_TOTAL",
            2: "C2_COUNT_MEN+",
            3: "C3_COUNT_WOMEN+",
            4: "C10_RATE_TOTAL",
            5: "C11_RATE_MEN+",
            6: "C12_RATE_WOMEN+"
        }

        if value not in columns:
            raise HTTPException(status_code=400, detail="Invalid value")

        column = columns[value]

        result = con.execute(
            f"""
            SELECT "{column}"
            FROM read_parquet(?)
            WHERE DGUID = ?
              AND CHARACTERISTIC_ID = ?
            """,
            [file, geo_code, char_id]
        ).fetchone()

        if result is None:
            raise HTTPException(
                status_code=404,
                detail="Population data not found"
            )

        return {
            "census_year": census_year,
            "geo_code": geo_code,
            "characteristic_id": char_id,
            "value": result[0]
        }

    else:
        raise HTTPException(
            status_code=400,
            detail="Unsupported census year"
        )