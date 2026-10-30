from fastapi.testclient import TestClient
import duckdb

from main import app
from models import PopulationBatchRequest

client = TestClient(app)

sample_dissemination_areas = [
    "10010145",  # Newfoundland and Labrador (PR 10)
    "12090103",  # Nova Scotia - Halifax (PR 12, CD 09)
    "24230012",  # Quebec - Montréal area (PR 24)
    "35190432",  # Ontario - York Region (PR 35, CD 19)
    "35210150",  # Ontario - Peel Region / Mississauga (PR 35, CD 21)
    "35390144",  # Ontario - Middlesex / London (PR 35, CD 39)
    "46110045",  # Manitoba (PR 46)
    "48060211",  # Alberta - Calgary area (PR 48, CD 06)
    "48110502",  # Alberta - Edmonton area (PR 48, CD 11)
    "59153621",  # British Columbia - Greater Vancouver (PR 59, CD 15)
    "60010015",  # Yukon (PR 60)
]

sample_da_dguids = [
    "2021S051610010001",
    "2021S051610010002",
    "2021S051610010003",
    "2021S051610010004",
    "2021S051610010005",
    "2021S051610010006",
    "2021S051610010007",
    "2021S051610010008",
    "2021S051610010009",
    "2021S051610010010",
]


def test_2021_population():
    batch_req = PopulationBatchRequest(
        census_year=2021,
        geo_codes=sample_da_dguids,
        char_id=1,
        value=1,
    )

    response = client.post(
        "/api/population_batch",
        json=batch_req.model_dump(),
    )

    assert response.status_code == 200

    data = response.json()["data"]
    boundaries = response.json()["boundaries"]

    assert len(data) > 0
    assert all("geo_code" in item for item in data)
    assert all("value" in item for item in data)
    assert len(boundaries) > 0


def test_2021_dguids_exist():
    db = duckdb.connect()

    rows = db.execute(
        """
        SELECT DGUID, CHARACTERISTIC_ID, C1_COUNT_TOTAL
        FROM read_parquet('parquet_data/2021_census_data.parquet')
        WHERE DGUID IN (
            SELECT UNNEST(?)
        )
        """,
        [sample_da_dguids],
    ).fetchall()

    db.close()

    assert len(rows) > 0


def test_2011_population():
    batch_req = PopulationBatchRequest(
        census_year=2011,
        geo_codes=sample_dissemination_areas,
        char_id=1,
        value=1,
    )
    response = client.post(
        "/api/population_batch",
        json=batch_req.model_dump(),
    )

    assert response.status_code == 200

    data = response.json()["data"]
    boundaries = response.json()["boundaries"]

    assert len(data) > 0
    assert all("geo_code" in item for item in data)
    assert all("value" in item for item in data)
    assert len(boundaries) > 0


sample_81_ct = [
    "9330243.00",
    "9330235.02",
    "9330235.01",
    "9330236.00",
    "9330242.00",
    "9330239.00",
    "9330230.02",
    "9330225.00",
]


def test_1981_population_no_char_for_geo():
    """
    For 1981 census tracts, characteristic id 3 is not valid.
    Should return a a list of NaN
    """
    batch_req = PopulationBatchRequest(
        census_year=1981,
        geo_codes=sample_81_ct,
        char_id=3,
        value=1,
    )

    response = client.post(
        "/api/population_batch",
        json=batch_req.model_dump(),
    )

    assert response.status_code == 200

    data = response.json()["data"]
    boundaries = response.json()["boundaries"]

    assert len(data) > 0
    assert data[0]["value"] == None
    assert data[0]["colour"] == [200, 200, 200]
    assert all("geo_code" in item for item in data)
    assert all("value" in item for item in data)
    assert all("value" in item for item in data)
    assert len(boundaries) == 0
