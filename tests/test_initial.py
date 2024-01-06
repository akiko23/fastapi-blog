import os

import pytest
from httpx import AsyncClient


def test_db_exits(db_path: str) -> None:
    assert os.path.exists(db_path)


@pytest.mark.asyncio
async def test_client(client: AsyncClient):
    resp = await client.get('/')
    assert resp.status_code == 200
    assert resp.json() == {"msg": "Welcome to FastAPI-blog!"}
