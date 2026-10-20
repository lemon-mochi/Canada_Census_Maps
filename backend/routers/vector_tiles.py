from fastapi import APIRouter, HTTPException, Depends

from models import GeoLevel, Tiles
from services.vector_tiles import vector_tile_path, geo_mappings
from pathlib import Path
from database import get_db


router = APIRouter()


@router.get(
    "/vector_tiles",
    response_model=Tiles,
)
def get_vector_tiles(
    census_year: int,
    geo_level: GeoLevel,
):
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


@router.get("/geo_mappings")
def get_geo_mappings(census_year: int, geo_level: str, db=Depends(get_db)):
    if census_year not in [1996, 2001, 2006]:
        raise HTTPException(status_code=400, detail="Unsupported census year")

    if geo_level not in ["Census tract", "Dissemination area"]:
        raise HTTPException(status_code=400, detail="Unsupported geography")

    path = Path(f"parquet_data/{census_year}_geographies.parquet")

    if not path.exists():
        raise HTTPException(status_code=404, detail="Parquet file not found")

    return geo_mappings(
        db=db,
        path=path,
        geo_level=geo_level,
    )
