from fastapi.testclient import TestClient
import types

from app.main import app


client = TestClient(app)


def _mock_response(status_code=200, json_data=None):
    resp = types.SimpleNamespace()
    resp.status_code = status_code
    resp.json = (lambda: json_data) if json_data is not None else (lambda: {})
    return resp


def test_healthz_ok():
    r = client.get("/healthz")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_movie_ok(monkeypatch):
    monkeypatch.setenv("OMDB_API_KEY", "test")

    payload = {
        "Title": "Inception",
        "Year": "2010",
        "Director": "Christopher Nolan",
        "Genre": "Action, Sci-Fi",
        "Plot": "A mind-bending heist.",
        "Ratings": [{"Source": "Internet Movie Database", "Value": "8.8/10"}],
        "Response": "True",
    }

    def fake_get(*args, **kwargs):
        return _mock_response(200, payload)

    import requests

    monkeypatch.setattr(requests, "get", fake_get)
    r = client.get("/movie", params={"title": "Inception"})
    assert r.status_code == 200
    body = r.json()
    assert body["title"] == "Inception"
    assert body["rating"] == "8.8/10"


def test_movie_not_found(monkeypatch):
    monkeypatch.setenv("OMDB_API_KEY", "test")

    payload = {"Response": "False", "Error": "Movie not found!"}

    def fake_get(*args, **kwargs):
        return _mock_response(200, payload)

    import requests

    monkeypatch.setattr(requests, "get", fake_get)
    r = client.get("/movie", params={"title": "DoesNotExist"})
    assert r.status_code == 404


def test_movie_upstream_error(monkeypatch):
    monkeypatch.setenv("OMDB_API_KEY", "test")

    import requests

    def fake_get(*args, **kwargs):
        raise requests.RequestException("boom")

    monkeypatch.setattr(requests, "get", fake_get)
    r = client.get("/movie", params={"title": "Inception"})
    assert r.status_code == 502
