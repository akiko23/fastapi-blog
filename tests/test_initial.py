import os

from fastapi.testclient import TestClient


def test_db_exits(db_path: str) -> None:
    assert os.path.exists(db_path)


def test_client(client: TestClient):
    resp = client.get('/')
    assert resp.status_code == 200
    assert resp.json() == {"msg": "Welcome to FastAPI-blog!"}
