from fastapi import APIRouter, HTTPException

from models import GeoLevel, Tiles
from services.vector_tiles import vector_tile_path

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