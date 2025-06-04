import pytest

@pytest.mark.asyncio
async def test_create_and_list_users(client):
    resp = await client.post(
        "/users",
        json={"email": "alice@example.com", "password": "secret"},
    )
    assert resp.status_code == 200, f"BAD RESPONSE: {resp.text}"
    data = resp.json()
    assert data["email"] == "alice@example.com"
    assert "id" in data

    resp = await client.get("/users")
    assert resp.status_code == 200
    users = resp.json()
    assert any(u["email"] == "alice@example.com" for u in users)


@pytest.mark.asyncio
async def test_create_and_list_items(client):
    # создаём пользователя
    resp = await client.post(
        "/users",
        json={"email": "bob@example.com", "password": "secret"},
    )
    assert resp.status_code == 200, f"USER CREATION FAILED: {resp.text}"
    owner_id = resp.json()["id"]

    # создаём элемент
    resp = await client.post(
        "/items",
        json={
            "title": "Item1",
            "description": "Description1",
            "owner_id": owner_id,
        },
    )
    assert resp.status_code == 200, f"ITEM CREATION FAILED: {resp.text}"
    item = resp.json()
    assert item["title"] == "Item1"
    assert item["owner_id"] == owner_id

    resp = await client.get("/items")
    assert resp.status_code == 200
    items = resp.json()
    assert any(i["title"] == "Item1" for i in items)
