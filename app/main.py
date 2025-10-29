from fastapi import FastAPI, HTTPException, Query
import requests
from functools import lru_cache
from typing import Any, Dict, List, Optional

app = FastAPI(title="GitHub Gists API")


@lru_cache(maxsize=128)
def fetch_gists(
    username: str, per_page: int, page: int
) -> Optional[List[Dict[str, Any]]]:
    """
    Fetch gists from the GitHub API with pagination.
    Results are cached in memory for repeated requests.
    """
    url = f"https://api.github.com/users/{username}/gists"
    params = {"per_page": per_page, "page": page}
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "fastapi-gists-app",
    }

    try:
        resp = requests.get(url, params=params, headers=headers, timeout=5)
    except requests.RequestException:
        return None

    if resp.status_code != 200:
        return None

    return resp.json()


@app.get("/{username}")
def get_gists(
    username: str,
    per_page: int = Query(
        10,
        gt=0,
        le=50,
        description="Number of gists per page",
    ),
    page: int = Query(
        1,
        gt=0,
        description="Page number",
    ),
):
    """
    Return a paginated list of filenames for a given user's public gists.
    """
    gists = fetch_gists(username, per_page, page)
    if gists is None:
        raise HTTPException(status_code=404, detail="User not found")

    filenames: List[str] = []
    for gist in gists:
        files = gist.get("files", {})
        filenames.extend(list(files.keys()))

    return {
        "user": username,
        "page": page,
        "per_page": per_page,
        "gists": filenames,
    }