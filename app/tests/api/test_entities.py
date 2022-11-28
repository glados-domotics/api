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
        room_id=kitchen.id,
    )
    entity.save(commit=False)

    entity = Entity(
        id=uuid.UUID(int=2),
        name="Lamp",
        type=constants.EntityType.light.name,
        status=constants.EntityStatus.on.name,
        value=200,
        room_id=living_room.id,
    )
    entity.save(commit=False)

    entity = Entity(
        id=uuid.UUID(int=3),
        name="Thermometer",
        type=constants.EntityType.sensor.name,
        status=constants.EntityStatus.on.name,
        value=28,
        room_id=living_room.id,
    )
    entity.save(commit=False)


# GET ##############################################################################################
def test_get_entities_with_invalid_data_sould_failed(client):
    response = client.get("/entities?type=invalid")

    assert response.status_code == 422
    assert response.json == {"errors": {
        "type": ["Must be one of: sensor, light, switch, multimedia, air_conditioner."]
    }}


def test_get_entities_sould_success(client, entities, mocker):
    response = client.get("/entities")

    assert response.status_code == 200
    assert response.json == [
        {
            "id": "00000000-0000-0000-0000-000000000001",
            "name": "Ceiling Light",
            "type": "light",
            "status": "off",
            "value": None,
            "created_at": mocker.ANY
        },
        {
            "id": "00000000-0000-0000-0000-000000000002",
            "name": "Lamp",
            "type": "light",
            "status": "on",
            "value": "200",
            "created_at": mocker.ANY
        },
        {
            "id": "00000000-0000-0000-0000-000000000003",
            "name": "Thermometer",
            "type": "sensor",
            "status": "on",
            "value": "28",
            "created_at": mocker.ANY
        }
    ]


def test_get_entities_with_type_filter_sould_success(client, entities, mocker):
    response = client.get("/entities?type=sensor")

    assert response.status_code == 200
    assert response.json == [
        {
            "id": "00000000-0000-0000-0000-000000000003",
            "name": "Thermometer",
            "type": "sensor",
            "status": "on",
            "value": "28",
            "created_at": mocker.ANY
        }
    ]


def test_get_entities_with_room_id_filter_sould_success(client, entities, mocker):
    response = client.get(f"/entities?room_id={uuid.UUID(int=1)}")

    assert response.status_code == 200
    assert response.json == [
        {
            "id": "00000000-0000-0000-0000-000000000001",
            "name": "Ceiling Light",
            "type": "light",
            "status": "off",
            "value": None,
            "created_at": mocker.ANY
        },
    ]


def test_get_entities_with_status_filter_sould_success(client, entities, mocker):
    response = client.get(f"/entities?status={constants.EntityStatus.off.name}")

    assert response.status_code == 200
    assert response.json == [
        {
            "id": "00000000-0000-0000-0000-000000000001",
            "name": "Ceiling Light",
            "type": "light",
            "status": "off",
            "value": None,
            "created_at": mocker.ANY
        },
    ]


def test_get_entities_with_matching_multiple_filter_sould_success(client, entities, mocker):
    response = client.get(
        f"/entities?type=light&room_id={uuid.UUID(int=2)}&status={constants.EntityStatus.on.name}"
    )

    assert response.status_code == 200
    assert response.json == [
        {
            "id": "00000000-0000-0000-0000-000000000002",
            "name": "Lamp",
            "type": "light",
            "status": "on",
            "value": "200",
            "created_at": mocker.ANY
        },
    ]


def test_get_entities_with_no_matching_multiple_filter_sould_success(client, entities, mocker):
    response = client.get(
        f"/entities?type=light&room_id={uuid.UUID(int=1)}&status={constants.EntityStatus.on.name}"
    )

    assert response.status_code == 200
    assert response.json == []


def test_get_filter_sould_success(client, entities, mocker):
    response = client.get(
        f"/filter"
    )

    assert response.status_code == 200
    assert response.json == [
        {
            "id": 1,
            "name": "Types",
            "choices": [
                {
                    "id": 1,
                    "name": "sensor"
                },
                {
                    "id": 2,
                    "name": "light"
                },
                {
                    "id": 3,
                    "name": "switch"
                },
                {
                    "id": 4,
                    "name": "multimedia"
                },
                {
                    "id": 5,
                    "name": "air_conditioner"
                }
            ]
        },
        {
            "id": 2,
            "name": "Status",
            "choices": [
                {
                    "id": 1,
                    "name": "on"
                },
                {
                    "id": 2,
                    "name": "off"
                },
                {
                    "id": 3,
                    "name": "unavailable"
                }
            ]
        }
    ]
