import uuid
import pytest

from glados.models import Entity, Room


@pytest.fixture
def entities():
    kitchen = Room(id=uuid.UUID(int=1), name="Kitchen")
    kitchen.save(commit=False)

    living_room = Room(id=uuid.UUID(int=2), name="Living Room")
    living_room.save(commit=False)

def test_get_rooms(client, entities):
    response = client.get("/rooms")

    assert response.status_code == 200
    assert response.json == [
        {
            "id": "00000000-0000-0000-0000-000000000001",
            "name": "Kitchen",
        },
        {
            "id": "00000000-0000-0000-0000-000000000002",
            "name": "Living Room",
        }
    ]

def test_create_rooms__missing_name(client, entities):
    response = client.post("/rooms", json = {})
    assert response.status_code == 422
    assert response.json == { "errors": { "name": [ "Missing data for required field." ] } }

def test_create_rooms(client, entities):
    response = client.post("/rooms", json = {
        'name' : 'test name'
    })
    assert response.status_code == 201

def test_remove_rooms(client, entities):
    response = client.delete("/rooms/00000000-0000-0000-0000-000000000001")
    assert response.status_code == 204

def test_update_rooms(client, entities):
    response = client.put("/rooms/00000000-0000-0000-0000-000000000002", json = {
        'name' : 'test name'
    })
    assert response.status_code == 204
