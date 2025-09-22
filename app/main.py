import os
import requests
from fastapi import FastAPI, HTTPException, Query
from mangum import Mangum

app = FastAPI(title="Film Finder API")

OMDB_URL = "http://www.omdbapi.com/"

def getOmdbApiKey() -> str:
    if apiKey := os.getenv("OMDB_API_KEY"):
        return apiKey
    else:
        raise RuntimeError("OMDB_API_KEY not set")

@app.get("/movie")
def getMovie(title: str = Query(..., min_length=1)):
    """Return cleaned movie details from OMDb."""
    params = {"t": title, "apikey": getOmdbApiKey(), "plot": "short"}
    r = requests.get(OMDB_URL, params=params, timeout=8)
    if r.status_code != 200:
        raise HTTPException(status_code=502, detail="Upstream error")
    data = r.json()
    if data.get("Response") != "True":
        raise HTTPException(status_code=404, detail=data.get("Error", "Not found"))
    return {
        "title": data.get("Title"),
        "year": data.get("Year"),
        "director": data.get("Director"),
        "rating": next((x["Value"] for x in data.get("Ratings", []) if x["Source"]=="Internet Movie Database"), None),
        "genre": data.get("Genre"),
        "plot": data.get("Plot"),
    }

handler = Mangum(app)