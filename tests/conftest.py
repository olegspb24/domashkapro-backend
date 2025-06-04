# tests/conftest.py
import asyncio

import pytest_asyncio
from httpx import AsyncClient
from httpx._transports.asgi import ASGITransport

from app.main import app
from app.db import engine, Base  # <-- убедитесь, что у вас именно так называется модуль с engine и Base

# 1) Синхронная фикстура event_loop с session-scope, чтобы её можно было юзать в других session-фикстурах
@pytest_asyncio.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

# 2) Один раз (session-авто) готовим базу: дропаем и создаём все таблицы
@pytest_asyncio.fixture(scope="session", autouse=True)
async def prepare_database(event_loop):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

# 3) Каждый тест получает настоящий AsyncClient с ASGITransport
@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as ac:
        yield ac
