from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

def test_2021_characteristics():
    response = client.get(
        "/api/characteristics",
        params={
            "census_year": 2021
        }
    )

    assert response.status_code == 200
    assert response.json() is not None
    assert len(response.json()) > 0

def test_2006_characteristics():
    response = client.get(
        "/api/characteristics",
        params={
            "census_year": 2006
        }
    )

    assert response.status_code == 200
    assert response.json() is not None
    assert len(response.json()) > 0

def test_characteristics_invalid_year():
    response = client.get(
        "/api/characteristics",
        params={
            "census_year": 2017
        }
    )

    assert response.status_code == 404

def test_characteristics_invalid_year_2():
    response = client.get(
        "/api/characteristics",
        params={
            "census_year": 2003
        }
    )

    assert response.status_code == 404