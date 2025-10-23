from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_octocat_gists_basic():
    """Test basic gists retrieval for octocat."""
    response = client.get("/octocat")
    assert response.status_code == 200

    data = response.json()
    assert data["user"] == "octocat"
    assert isinstance(data["gists"], list)
    assert len(data["gists"]) > 0


def test_octocat_gists_pagination():
    """Test pagination parameters."""
    # Page 1, 2 gists per page
    response1 = client.get("/octocat?per_page=2&page=1")
    assert response1.status_code == 200
    data1 = response1.json()
    assert data1["per_page"] == 2
    assert data1["page"] == 1
    assert isinstance(data1["gists"], list)
    assert len(data1["gists"]) <= 2  # max 2 items

    # Page 2, 2 gists per page
    response2 = client.get("/octocat?per_page=2&page=2")
    assert response2.status_code == 200
    data2 = response2.json()
    assert data2["per_page"] == 2
    assert data2["page"] == 2
    assert isinstance(data2["gists"], list)
    assert len(data2["gists"]) <= 2

    # The two pages should not be identical if octocat has >= 4 gists
    if len(data1["gists"]) > 0 and len(data2["gists"]) > 0:
        assert data1["gists"] != data2["gists"]


def test_invalid_user():
    """Test invalid GitHub username returns 404."""
    response = client.get("/thisuserdoesnotexist123456")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "User not found"
