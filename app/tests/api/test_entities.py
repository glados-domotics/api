import uuid
import pytest

from glados import constants
from glados.models import Entity, Room


@pytest.fixture
def entities():
    kitchen = Room(id=uuid.UUID(int=1), name="Kitchen")
    kitchen.save(commit=False)

    living_room = Room(id=uuid.UUID(int=2), name="Living Room")
    living_room.save(commit=False)

    entity = Entity(
        id=uuid.UUID(int=1),
        name="Ceiling Light",
        type=constants.EntityType.light.name,
        status=constants.EntityStatus.off.name,
        value=None,
        room_id=kitchen.id
    )
    entity.save(commit=False)

    entity = Entity(
        id=uuid.UUID(int=2),
        name="Lamp",
        type=constants.EntityType.light.name,
        status=constants.EntityStatus.on.name,
        value=200,
        room_id=living_room.id)
    entity.save(commit=False)

    entity = Entity(
        id=uuid.UUID(int=3),
        name="Thermometer",
        type=constants.EntityType.sensor.name,
        status=constants.EntityStatus.on.name,
        value=28,
        room_id=living_room.id)
    entity.save(commit=False)


def test_get_entities_with_invalid_data(client):
    response = client.get("/entities?type=invalid")

    assert response.status_code == 422
    assert response.json == {"errors": {
        "type": ["Must be one of: sensor, light, switch, multimedia, air_conditioner."]
    }}


def test_get_entities(client, entities, mocker):
    response = client.get("/entities")

    assert response.status_code == 200
    assert response.json == [
        {
            "id": "00000000-0000-0000-0000-000000000001",
            "name": "Ceiling Light",
            "type": "light",
            "status": "off",
            "value": None,
            "created_at": mocker.ANY,
            "room": mocker.ANY
        },
        {
            "id": "00000000-0000-0000-0000-000000000002",
            "name": "Lamp",
            "type": "light",
            "status": "on",
            "value": "200",
            "created_at": mocker.ANY,
            "room": mocker.ANY
        },
        {
            "id": "00000000-0000-0000-0000-000000000003",
            "name": "Thermometer",
            "type": "sensor",
            "status": "on",
            "value": "28",
            "created_at": mocker.ANY,
            "room": mocker.ANY
        }
    ]


def test_get_entities_with_type_filter(client, entities, mocker):
    response = client.get("/entities?type=sensor")

    assert response.status_code == 200
    assert response.json == [
        {
            "id": "00000000-0000-0000-0000-000000000003",
            "name": "Thermometer",
            "type": "sensor",
            "status": "on",
            "value": "28",
            "created_at": mocker.ANY,
            "room": mocker.ANY
        }
    ]

def test_get_entities_with_invalid_data_status(client):
    response = client.get("/entities?status=invalid")

    assert response.status_code == 422
    assert response.json == {"errors": {
        "status": ["Must be one of: on, off, unavailable."]
    }}

def test_get_entities_with_status_filter(client, entities, mocker):
    response = client.get("/entities?status=on")

    assert response.status_code == 200
    assert response.json == [
        {
            "id": "00000000-0000-0000-0000-000000000002",
            "name": "Lamp",
            "type": "light",
            "status": "on",
            "value": "200",
            "created_at": mocker.ANY,
            "room": mocker.ANY
        },
        {
            "id": "00000000-0000-0000-0000-000000000003",
            "name": "Thermometer",
            "type": "sensor",
            "status": "on",
            "value": "28",
            "created_at": mocker.ANY,
            "room": mocker.ANY
        }
    ]

def test_get_entities_with_invalid_data_status(client):
    response = client.get("/entities?room=invalid")

    assert response.status_code == 422
    assert response.json == {"errors": {
        "room": ["Not a valid UUID."]
    }}

def test_get_entities_with_room_filter(client, entities, mocker):
    response = client.get("/entities?room=00000000-0000-0000-0000-000000000001")

    assert response.status_code == 200
    assert response.json == [
        {
            "id": "00000000-0000-0000-0000-000000000001",
            "name": "Ceiling Light",
            "type": "light",
            "status": "off",
            "value": None,
            "created_at": mocker.ANY,
            "room": mocker.ANY
        }
    ]
def test_create_entity(client, entities):
    response = client.post("/entities", json = {
        "name": "test name",
        "type": "sensor",
        "status": "off",
        "room": "00000000-0000-0000-0000-000000000001",
    })
    assert response.status_code == 201

def test_remove_rooms(client, entities):
    response = client.delete("/entities/00000000-0000-0000-0000-000000000001")
    assert response.status_code == 204

def test_update_rooms(client, entities):
    response = client.put("/entities/00000000-0000-0000-0000-000000000002", json = {
        "name": "test name",
        "type": "sensor",
        "status": "off",
        "room": "00000000-0000-0000-0000-000000000001",
    })
    assert response.status_code == 204
