from fastapi import APIRouter

from models import Characteristic
from services.census import load_characteristics

router = APIRouter()


@router.get(
    "/characteristics",
    response_model=list[Characteristic],
)
def get_characteristics(census_year: int):
    return load_characteristics(census_year)


@router.get("/columns")
def get_columns(census_year: int, char_id: int):
    for characteristic in load_characteristics(census_year):
        if characteristic["CHARACTERISTIC_ID"] == char_id:
            return [
                {"column_id": column["column_id"]}
                for column in characteristic["columns"]
            ]

    from fastapi import HTTPException

    raise HTTPException(
        status_code=404,
        detail="Characteristic not found",
    )