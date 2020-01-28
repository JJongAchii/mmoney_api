import json
import pytest

from app.api import countries

def test_create_country(test_app, monkeypatch):
  test_payload = {"name": "Cambodia"}
  test_resp = {"id": 1, "name": "Cambodia"}

  async def mock_post(payload):
    return 1
  
  monkeypatch.setattr(countries, "post", mock_post)

  response = test_app.post("/countries", data=json.dumps(test_payload),)
  assert response.status_code == 201
  assert response.json() == test_resp

def test_create_invalid_country(test_app):
  response = test_app.post("/countries", data=json.dumps({"title": "something"}))
  assert response.status_code == 422

def test_get_country(test_app, monkeypatch):
  test_data = {"id": 2, "name": "Russia"}

  async def mock_get(id):
    return test_data

  monkeypatch.setattr(countries, "get", mock_get)

  response = test_app.get("/countries/2")
  assert response.status_code == 200
  assert response.json() == test_data

def test_non_existent_country(test_app, monkeypatch):
  async def mock_get(id):
    return None
  
  monkeypatch.setattr(countries, "get", mock_get)

  response = test_app.get("/countries/12")
  assert response.status_code == 404
  assert response.json()["detail"] == "Country Not Found"

def test_get_all_countries(test_app, monkeypatch):
  test_all_countries = [
    {"id": 1, "name": "Uganda"},
    {"id": 2, "name": "Tanzania"}
  ]

  async def mock_get_all():
    return test_all_countries
  monkeypatch.setattr(countries, "get_all", mock_get_all)

  response = test_app.get("/countries")
  assert response.status_code == 200
  assert response.json() == test_all_countries
