"""
Basic smoke tests — extend these as you build your CI/CD pipeline.
Run: pytest test_main.py -v
"""
import pytest
from fastapi.testclient import TestClient

from database import init_db
from main import app

# Initialise DB once before any tests run
init_db()

client = TestClient(app)

DUMMY_EMAIL = "test@example.com"
DUMMY_PASS = "securepass123"


@pytest.fixture(autouse=True)
def clean_users():
    """Wipe users table before each test for a clean slate."""
    from database import get_connection
    conn = get_connection()
    conn.execute("DELETE FROM users")
    conn.commit()
    conn.close()
    yield


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_register_success():
    r = client.post("/register", json={"email": DUMMY_EMAIL, "password": DUMMY_PASS})
    assert r.status_code == 201


def test_register_duplicate():
    client.post("/register", json={"email": DUMMY_EMAIL, "password": DUMMY_PASS})
    r = client.post("/register", json={"email": DUMMY_EMAIL, "password": DUMMY_PASS})
    assert r.status_code == 409


def test_register_short_password():
    r = client.post("/register", json={"email": "short@test.com", "password": "abc"})
    assert r.status_code == 422


def test_login_success():
    client.post("/register", json={"email": DUMMY_EMAIL, "password": DUMMY_PASS})
    r = client.post("/login", json={"email": DUMMY_EMAIL, "password": DUMMY_PASS})
    assert r.status_code == 200
    assert "access_token" in r.json()


def test_login_wrong_password():
    client.post("/register", json={"email": DUMMY_EMAIL, "password": DUMMY_PASS})
    r = client.post("/login", json={"email": DUMMY_EMAIL, "password": "wrongpass"})
    assert r.status_code == 401


def test_me_authenticated():
    client.post("/register", json={"email": DUMMY_EMAIL, "password": DUMMY_PASS})
    token = client.post("/login", json={"email": DUMMY_EMAIL, "password": DUMMY_PASS}).json()["access_token"]
    r = client.get("/me", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200
    assert r.json()["email"] == DUMMY_EMAIL


def test_me_no_token():
    # HTTPBearer returns 403 when Authorization header is missing entirely
    r = client.get("/me")
    assert r.status_code in (401, 403)  # depends on FastAPI version


def test_me_bad_token():
    r = client.get("/me", headers={"Authorization": "Bearer notavalidtoken"})
    assert r.status_code == 401
