import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_client(client: AsyncClient):
    resp = await client.get("/")
    assert resp.status_code == 200
    assert resp.json() == {"msg": "Welcome to FastAPI-blog!"}
