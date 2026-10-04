from fastapi import APIRouter, Depends, HTTPException, Query

import colour_data

from config import GEO_TABLE, MAIN_TABLE, NHS_DA_YEAR
from database import get_db
from models import GeoLevel, PopulationValue
from services.census import (
    legacy_value,
    read_required,
    stored_value,
    two_sex_value,
    year_files,
)

router = APIRouter()


@router.get("/population")
def get_population(
    geo_level: GeoLevel,
    char_id: int,
    db=Depends(get_db),
):
    levels = (
        ("Province", "Territory")
        if geo_level == "Province"
        else (geo_level,)
    )

    placeholders = ",".join("?" * len(levels))

    result = db.execute(
        f"""
        SELECT m.DGUID, m.C1_COUNT_TOTAL
        FROM read_parquet(?) AS m
        JOIN read_parquet(?) AS g
            ON m.DGUID = g.DGUID
        WHERE g.GEO_LEVEL IN ({placeholders})
          AND m.CHARACTERISTIC_ID = ?
        """,
        [
            str(MAIN_TABLE),
            str(GEO_TABLE),
            *levels,
            char_id,
        ],
    ).fetchdf()

    coloured = colour_data.assign_colours(
        df=result,
        num_colours=3,
        equal_width=True,
        col="C1_COUNT_TOTAL",
    )

    return coloured.to_dict(orient="records")


@router.get(
    "/specific_population",
    response_model=PopulationValue,
)
def get_specific_population(
    census_year: int,
    geo_code: str,
    char_id: int,
    value: int = Query(..., ge=1, le=6),
    db=Depends(get_db),
):
    file = year_files(census_year).data

    if not file.exists():
        raise HTTPException(
            status_code=404,
            detail=f"Invalid census year: {census_year}",
        )

    if census_year <= NHS_DA_YEAR:
        result = legacy_value(
            db,
            census_year,
            file,
            geo_code,
            char_id,
            value,
        )

    elif census_year in (2011, 2016):
        result = two_sex_value(
            db,
            file,
            geo_code,
            char_id,
            value,
        )

    elif census_year == 2021:
        result = stored_value(
            db,
            file,
            geo_code,
            char_id,
            value,
        )

    else:
        raise HTTPException(
            status_code=400,
            detail="Unsupported census year",
        )

    return PopulationValue(
        census_year=census_year,
        geo_code=geo_code,
        characteristic_id=char_id,
        value=result,
    )