# FastAPI GitHub Gists API

## Project Overview

This project implements a **REST API** using **FastAPI** to list all publicly available **GitHub Gists for a given user**.  

#### Key features

- **Pagination** – Retrieve a specific page of gists with a limited number per page.
- **Caching** – In-memory caching using `functools.lru_cache` to reduce repeated GitHub API calls.
- **Dockerized** – Runs inside a container on port 8080.
- **Automated Testing** – Uses `pytest` to verify API functionality.


#### Example API Endpoint

*Request*
```bash
GET /octocat?per_page=5&page=2
```

*Response*
```json
{
  "user": "octocat",
  "page": 2,
  "per_page": 5,
  "gists": ["hello_world.py", "readme.md"]
}
```

#### Project Structure

```yaml
fastapi-gists-app/
│── app/
│ ├── __init__.py         # marks app as Python package
│ └── main.py         # FastAPI application code
│── tests/
│ ├── __init__.py
│ └── test_gists.py   # pytest test cases
│── requirements.txt
│── Dockerfile
│── .gitignore
│── README.md
```


---

## Prerequisites

- Python 3.7+
- pip
- Docker (optional, for containerized deployment)

---

## Setup Instructions

### 0. Create Project Folder

```bash
git clone <REPO_URL> fastapi-gists-app
cd fastapi-gists-app
```

### 1. Create and activate virtual environment

```bash
python -m venv .venv
.venv\Scripts\activate       # Windows
source .venv/bin/activate    # Mac/Linux
```

### 2. Install dependencies
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Run the API locally
```bash
uvicorn app.main:app --reload --port 8080
```

Swagger UI : [http://localhost:8080/docs](http://localhost:8080/docs)

Example Call : [http://localhost:8080/octocat](http://localhost:8080/octocat)

Paginated Call : [http://localhost:8080/octocat?per_page=5&page=2](http://localhost:8080/octocat?per_page=5&page=2)

### 4. Running Tests

#### Automated tests verify

 - Retrieval of public gists for a user
 - Pagination functionality
 - Handling of invalid GitHub usernames

#### Run tests locally
```bash
pytest -v
```

### 5. Docker Instructions
#### 1. Build Docker image
```bash
docker build -t fastapi-gists .
```

#### 2. Run container
```bash
docker run -p 8080:8080 fastapi-gists
```

Access API : [http://localhost:8080/octocat](http://localhost:8080/octocat)

Paginated Example : [http://localhost:8080/octocat?per_page=3&page=2](http://localhost:8080/octocat?per_page=3&page=2)

#### 3. Run container in detached mode
```bash
docker run -d -p 8080:8080 fastapi-gists
docker logs <container_id>
```

#### 4. Run tests inside Docker
```bash
docker run --rm -it fastapi-gists pytest -v
```

---

## Code Features

- **FastAPI** – modern Python web framework for APIs
- **Requests** – interacts with GitHub API
- **Caching** – reduces repeated API calls
- **Pagination** – controlled via page and per_page query parameters
- **Automated Tests** – using pytest and fastapi.testclient
- **Dockerized** – easy deployment

---

## Notes

```markdown
- Pagination ensures the API can handle users with many gists without overloading memory.
- In-memory caching improves performance; for production, consider Redis or another persistent cache.
- API is designed to be modular and easy to extend.
```

---