from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_1981_total_count():
    response = client.get(
        "/api/specific_population",
        params={
            "census_year": 1981,
            "geo_code": "00",
            "char_id": 2,
            "value": 1,
        },
    )

    assert response.status_code == 200
    assert response.json()["value"] is not None


def test_1981_total_rate():
    response = client.get(
        "/api/specific_population",
        params={
            "census_year": 1981,
            "geo_code": "00",
            "char_id": 10,
            "value": 4,
        },
    )

    assert response.status_code == 200
    assert response.json()["value"] is not None


def test_1981_invalid_male_count():
    response = client.get(
        "/api/specific_population",
        params={
            "census_year": 1981,
            "geo_code": "00",
            "char_id": 10,
            "value": 2,
        },
    )

    assert response.status_code == 400


def test_2011_total_count():
    response = client.get(
        "/api/specific_population",
        params={
            "census_year": 2011,
            "geo_code": "01",
            "char_id": 10,
            "value": 1,
        },
    )

    assert response.status_code == 200
    assert response.json()["value"] is not None


def test_2011_male_count():
    response = client.get(
        "/api/specific_population",
        params={
            "census_year": 2011,
            "geo_code": "01",
            "char_id": 10,
            "value": 2,
        },
    )

    assert response.status_code == 200
    assert response.json()["value"] is not None


def test_2011_female_count():
    response = client.get(
        "/api/specific_population",
        params={
            "census_year": 2011,
            "geo_code": "01",
            "char_id": 10,
            "value": 3,
        },
    )

    assert response.status_code == 200
    assert response.json()["value"] is not None


def test_2011_total_rate():
    response = client.get(
        "/api/specific_population",
        params={
            "census_year": 2011,
            "geo_code": "01",
            "char_id": 10,
            "value": 4,
        },
    )

    assert response.status_code == 200
    assert response.json()["value"] is not None


def test_2011_male_rate():
    response = client.get(
        "/api/specific_population",
        params={
            "census_year": 2011,
            "geo_code": "01",
            "char_id": 10,
            "value": 5,
        },
    )

    assert response.status_code == 200
    assert response.json()["value"] is not None


def test_2011_female_rate():
    response = client.get(
        "/api/specific_population",
        params={
            "census_year": 2011,
            "geo_code": "01",
            "char_id": 10,
            "value": 6,
        },
    )

    assert response.status_code == 200
    assert response.json()["value"] is not None


def test_2016_total_rate():
    response = client.get(
        "/api/specific_population",
        params={
            "census_year": 2016,
            "geo_code": "01",
            "char_id": 10,
            "value": 4,
        },
    )

    assert response.status_code == 200
    assert response.json()["value"] is not None


def test_2021_total_count():
    response = client.get(
        "/api/specific_population",
        params={
            "census_year": 2021,
            "geo_code": "2021A000011124",
            "char_id": 1,
            "value": 1,
        },
    )

    assert response.status_code == 200
    assert response.json()["value"] is not None


def test_2021_male_count():
    response = client.get(
        "/api/specific_population",
        params={
            "census_year": 2021,
            "geo_code": "2021A000011124",
            "char_id": 8,
            "value": 2,
        },
    )

    assert response.status_code == 200
    assert response.json()["value"] is not None


def test_2021_female_count():
    response = client.get(
        "/api/specific_population",
        params={
            "census_year": 2021,
            "geo_code": "2021A000011124",
            "char_id": 8,
            "value": 3,
        },
    )

    assert response.status_code == 200
    assert response.json()["value"] is not None


def test_2021_total_rate():
    response = client.get(
        "/api/specific_population",
        params={
            "census_year": 2021,
            "geo_code": "2021A000011124",
            "char_id": 10,
            "value": 4,
        },
    )

    assert response.status_code == 200
    assert response.json()["value"] is not None


def test_2021_male_rate():
    response = client.get(
        "/api/specific_population",
        params={
            "census_year": 2021,
            "geo_code": "2021A000011124",
            "char_id": 8,
            "value": 5,
        },
    )

    assert response.status_code == 200
    assert response.json()["value"] is not None


def test_2021_female_rate():
    response = client.get(
        "/api/specific_population",
        params={
            "census_year": 2021,
            "geo_code": "2021A000011124",
            "char_id": 8,
            "value": 6,
        },
    )

    assert response.status_code == 200
    assert response.json()["value"] is not None


def test_2001_invalid_male_count():
    response = client.get(
        "/api/specific_population",
        params={
            "census_year": 2001,
            "geo_code": "01",
            "char_id": 10,
            "value": 2,
        },
    )

    assert response.status_code == 400


def test_invalid_characteristic():
    response = client.get(
        "/api/specific_population",
        params={
            "census_year": 2021,
            "geo_code": "2021A000011124",
            "char_id": 999999,
            "value": 1,
        },
    )

    assert response.status_code == 404


def test_invalid_value():
    response = client.get(
        "/api/specific_population",
        params={
            "census_year": 2021,
            "geo_code": "2021A000011124",
            "char_id": 1,
            "value": 7,
        },
    )

    assert response.status_code == 400

def test_invalid_column_2021():
    response = client.get(
        "/api/specific_population",
        params={
            "census_year": 2021,
            "geo_code": "01",
            "char_id": 1,
            "value": 2
        }
    )

    assert response.status_code == 404

def test_2011_nhs_da_count():
    response = client.get(
        "api/specific_population",
        params={
            "census_year": 2010, # 2010 is for 2011 NHS DAs
            "geo_code": "10010732",
            "char_id": 5,
            "value": 1
        }
    )

    assert response.status_code == 200
    assert response.json()["value"] is not None

def test_2011_nhs_da_rate():
    response = client.get(
        "api/specific_population",
        params={
            "census_year": 2010, # 2010 is for 2011 NHS DAs
            "geo_code": "10010732",
            "char_id": 5,
            "value": 4
        }
    )

    assert response.status_code == 200
    assert response.json()["value"] is not None

def test_invalid_year_fail():
    response = client.get(
        "/api/specific_population",
        params={
            "census_year": 1998,
            "geo_code": "01",
            "char_id": 1,
            "value": 2
        }
    )

    assert response.status_code == 404    