import os
import requests
from fastapi import FastAPI, HTTPException, Query
from mangum import Mangum

app = FastAPI(title="Film Finder API")

MY_DIRECTORY = os.path.expanduser("~")
OMDB_URL = "https://www.omdbapi.com/"

def getOmdbApiKey() -> str:
    with open(os.path.join(MY_DIRECTORY, '.secret', 'file.txt')) as f:
        API_KEY = f.read()

    return API_KEY

@app.get("/movie")
def getMovie(title: str = Query(..., min_length=1)):
    """Return cleaned movie details from OMDb."""
    params = {"t": title, "apikey": getOmdbApiKey(), "plot": "short"}
    try:
        r = requests.get(OMDB_URL, params=params, timeout=8)
    except requests.RequestException:
        raise HTTPException(status_code=502, detail="Upstream error")
    if r.status_code != 200:
        raise HTTPException(status_code=502, detail="Upstream error")
    data = r.json()
    if data.get("Response") != "True":
        raise HTTPException(status_code=404, detail=data.get("Error", "Not found"))
    res = {
        "title": data.get("Title"),
        "year": data.get("Year"),
        "director": data.get("Director"),
        "rating": next((x["Value"] for x in data.get("Ratings", []) if x["Source"]=="Internet Movie Database"), None),
        "genre": data.get("Genre"),
        "plot": data.get("Plot"),
        "cast": data.get("Cast")
    }

    return res

    # for key, value in res.items():
    #     yield f"{key}: {value}\n"

@app.get("/healthz")
def healthz():
    return {"status": "ok"}

handler = Mangum(app)
