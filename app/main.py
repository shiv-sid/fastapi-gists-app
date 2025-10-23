from fastapi import FastAPI, HTTPException, Query
import requests
from functools import lru_cache

app = FastAPI(title="GitHub Gists API")

# In-memory cache for GitHub responses
@lru_cache(maxsize=128)
def fetch_gists(username: str, per_page: int, page: int):
    """
    Fetch gists from GitHub API with pagination.
    Caches results in memory for repeated requests.
    """
    url = f"https://api.github.com/users/{username}/gists?per_page={per_page}&page={page}"
    response = requests.get(url)

    if response.status_code != 200:
        return None
    return response.json()


@app.get("/{username}")
def get_gists(
    username: str,
    per_page: int = Query(10, gt=0, le=50, description="Number of gists per page"),
    page: int = Query(1, gt=0, description="Page number"),
):
    """
    Return a paginated list of filenames for a given GitHub user's public gists.
    """
    gists = fetch_gists(username, per_page, page)
    if gists is None:
        raise HTTPException(status_code=404, detail="User not found")

    filenames = [file for gist in gists for file in gist["files"].keys()]
    return {"user": username, "page": page, "per_page": per_page, "gists": filenames}
