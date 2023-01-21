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
        room_id=kitchen.id)
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
            "room_id": "00000000-0000-0000-0000-000000000001",
            "room" : {
                "id": "00000000-0000-0000-0000-000000000001",
                "name": "Kitchen",
                "created_at": mocker.ANY
            },
            "created_at": mocker.ANY
        },
        {
            "id": "00000000-0000-0000-0000-000000000002",
            "name": "Lamp",
            "type": "light",
            "status": "on",
            "value": "200",
            "room_id": "00000000-0000-0000-0000-000000000002",
            "room" : {
                "id": "00000000-0000-0000-0000-000000000002",
                "name": "Living Room",
                "created_at": mocker.ANY
            },
            "created_at": mocker.ANY
        },
        {
            "id": "00000000-0000-0000-0000-000000000003",
            "name": "Thermometer",
            "type": "sensor",
            "status": "on",
            "value": "28",
            "room_id": "00000000-0000-0000-0000-000000000002",
            "room" : {
                "id": "00000000-0000-0000-0000-000000000002",
                "name": "Living Room",
                "created_at": mocker.ANY
            },
            "created_at": mocker.ANY
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
            "room_id": "00000000-0000-0000-0000-000000000002",
            "room" : {
                "id": "00000000-0000-0000-0000-000000000002",
                "name": "Living Room",
                "created_at": mocker.ANY
            },
            "created_at": mocker.ANY
        }
    ]


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
            "room_id": "00000000-0000-0000-0000-000000000002",
            "room" : {
                "id": "00000000-0000-0000-0000-000000000002",
                "name": "Living Room",
                "created_at": mocker.ANY
            },
            "created_at": mocker.ANY
        },
        {
            "id": "00000000-0000-0000-0000-000000000003",
            "name": "Thermometer",
            "type": "sensor",
            "status": "on",
            "value": "28",
            "room_id": "00000000-0000-0000-0000-000000000002",
            "room" : {
                "id": "00000000-0000-0000-0000-000000000002",
                "name": "Living Room",
                "created_at": mocker.ANY
            },
            "created_at": mocker.ANY
        }
    ]


def test_get_entities_with_status_and_type_filters(client, entities, mocker):
    """
    Should returns filtered entries if both parameters are applied
    """
    response = client.get("/entities?status=on&type=sensor")

    assert response.status_code == 200
    assert response.json == [
        {
            "id": "00000000-0000-0000-0000-000000000003",
            "name": "Thermometer",
            "type": "sensor",
            "status": "on",
            "value": "28",
            "room_id": "00000000-0000-0000-0000-000000000002",
            "room" : {
                "id": "00000000-0000-0000-0000-000000000002",
                "name": "Living Room",
                "created_at": mocker.ANY
            },
            "created_at": mocker.ANY
        }
    ]


def test_get_entities_with_invalid_room_id_length(client):
    response = client.get("/entities?room_id=d9ec9a2f-6fd7-4e3c-ad29-7e293dcaa18d1")

    assert response.status_code == 422
    assert response.json == {"errors": {
        "room_id": ["The room_id length is incorrect; it should be 36 characters (UUID4 length). 37 characters were provided"]
    }}


def test_get_entities_with_wrong_room_id(client, entities):
    """
    Should returns filtered entries if both parameters are applied
    """
    response = client.get("/entities?room_id=" + str(uuid.UUID(int=3)))

    assert response.status_code == 200
    assert response.json == []


def test_get_one_entitiy(client, entities, mocker):
    """
    Should returns th one entry
    """
    response = client.get("/entities/00000000-0000-0000-0000-000000000003")

    assert response.status_code == 200
    assert response.json == {
        "id": "00000000-0000-0000-0000-000000000003",
        "name": "Thermometer",
        "type": "sensor",
        "status": "on",
        "value": "28",
        "room_id": "00000000-0000-0000-0000-000000000002",
        "room" : {
            "id": "00000000-0000-0000-0000-000000000002",
            "name": "Living Room",
            "created_at": mocker.ANY
        },
        "created_at": mocker.ANY
    }


def test_get_one_entitiy_with_wrong_id(client, entities):
    """
    Should return an error message with 404 status
    """
    response = client.get("/entities/0ed43070-86d4-4ed1-b03c-f88763ec5045")

    assert response.status_code == 404
    assert response.json == {"message": "Entity 0ed43070-86d4-4ed1-b03c-f88763ec5045 doesn't exist"}
