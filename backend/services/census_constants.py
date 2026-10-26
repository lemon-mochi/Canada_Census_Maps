from dataclasses import dataclass
from pathlib import Path

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
