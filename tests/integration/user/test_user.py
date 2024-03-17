import pytest
from fastapi_users.jwt import generate_jwt
from httpx import AsyncClient

from fastapi_blog.config import Config
from fastapi_blog.entity.users.schemas import UserCreate
from fastapi_blog.entity.users.service import UserService


@pytest.mark.asyncio
async def test_get_me(client: AsyncClient, user_service: UserService, config: Config):
    user = await user_service.create(
        UserCreate(email="user227@mail.ru", username="user226", password="12345")
    )

    token = generate_jwt(
        data={
            "sub": str(user.id),
            "email": user.email,
            "aud": "fastapi-users:auth",
        },
        secret=config.app.jwt_secret,
        lifetime_seconds=user_service.verification_token_lifetime_seconds,
    )
    resp = await client.get("users/me", headers={"Authorization": f"Bearer {token}"})

    got = resp.json()
    expected = {
        "id": user.id,
        "email": user.email,
        "username": user.username,
        "is_active": user.is_active,
        "is_superuser": user.is_superuser,
        "is_verified": user.is_verified,
        "registered_at": user.registered_at.isoformat(),
    }

    assert got == expected


@pytest.mark.asyncio
async def test_patch_me(client: AsyncClient, user_service: UserService, config: Config):
    user = await user_service.create(
        UserCreate(email="user228@mail.ru", username="user227", password="12345")
    )

    new_email = "user228@gmail.com"
    new_username = "new_user227"

    token = generate_jwt(
        data={
            "sub": str(user.id),
            "email": user.email,
            "aud": "fastapi-users:auth",
        },
        secret=config.app.jwt_secret,
        lifetime_seconds=user_service.verification_token_lifetime_seconds,
    )
    resp = await client.patch(
        url="users/me",
        headers={"Authorization": f"Bearer {token}"},
        json={"email": new_email, "username": new_username},
    )

    got = resp.json()
    expected = {
        "id": user.id,
        "email": new_email,
        "username": new_username,
        "is_active": user.is_active,
        "is_superuser": user.is_superuser,
        "is_verified": user.is_verified,
        "registered_at": user.registered_at.isoformat(),
    }

    assert got == expected


@pytest.mark.asyncio
async def test_get_user(client: AsyncClient, user_service: UserService, config: Config):
    common_user = await user_service.create(
        UserCreate(
            email="common_user@mail.ru", username="common_user226", password="12345"
        )
    )
    super_user = await user_service.create(
        UserCreate(
            email="admin@mail.ru",
            username="admin226",
            password="123456",
            is_superuser=True,
        )
    )

    common_user_token = generate_jwt(
        data={
            "sub": str(common_user.id),
            "email": common_user.email,
            "aud": "fastapi-users:auth",
        },
        secret=config.app.jwt_secret,
        lifetime_seconds=user_service.verification_token_lifetime_seconds,
    )
    superuser_token = generate_jwt(
        data={
            "sub": str(super_user.id),
            "email": super_user.email,
            "aud": "fastapi-users:auth",
        },
        secret=config.app.jwt_secret,
        lifetime_seconds=user_service.verification_token_lifetime_seconds,
    )

    # common user can't get info about other users
    cu_resp = await client.get(
        f"users/{super_user.id}",
        headers={"Authorization": f"Bearer {common_user_token}"},
    )

    got = cu_resp.json()
    expected = {"detail": "Forbidden"}

    assert got == expected

    # superuser can get info about any user
    su_resp = await client.get(
        f"users/{common_user.id}",
        headers={"Authorization": f"Bearer {superuser_token}"},
    )

    got = su_resp.json()
    expected = {
        "id": common_user.id,
        "email": common_user.email,
        "username": common_user.username,
        "is_active": common_user.is_active,
        "is_superuser": common_user.is_superuser,
        "is_verified": common_user.is_verified,
        "registered_at": common_user.registered_at.isoformat(),
    }

    assert got == expected
