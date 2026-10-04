from typing import Literal, Optional

from pydantic import BaseModel


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
    "Aggregate dissemination area",
    "Dissemination area",
]


class Column(BaseModel):
    column_id: int
    column_name: Optional[str] = None


class Characteristic(BaseModel):
    CHARACTERISTIC_ID: int
    CHARACTERISTIC_NAME: str
    level: int
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