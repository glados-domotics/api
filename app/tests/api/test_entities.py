import uuid
import pytest

from glados import constants
from glados.models import Entity, Room


class TestEntities:
    kitchen_id = uuid.uuid4()
    living_room_id = uuid.uuid4()

    @pytest.fixture
    def entities(self):

        kitchen = Room(id=self.kitchen_id, name="Kitchen")
        kitchen.save(commit=False)

        living_room = Room(id=self.living_room_id, name="Living Room")
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

    def test_get_entities_with_invalid_filter_values(self, client):
        response = client.get("/entities?type=invalid")
        assert response.status_code == 422
        assert response.json == {"errors": {
            "type": ["Must be one of: sensor, light, switch, multimedia, air_conditioner."]
        }}

        response = client.get("/entities?status=o")
        assert response.status_code == 422
        assert response.json == {"errors": {
            "status": ["Must be one of: on, off, unavailable."]
        }}

    def test_get_entities(self, client, entities, mocker):
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
                "room_id": str(self.kitchen_id)
            },
            {
                "id": "00000000-0000-0000-0000-000000000002",
                "name": "Lamp",
                "type": "light",
                "status": "on",
                "value": "200",
                "created_at": mocker.ANY,
                "room_id": str(self.living_room_id)
            },
            {
                "id": "00000000-0000-0000-0000-000000000003",
                "name": "Thermometer",
                "type": "sensor",
                "status": "on",
                "value": "28",
                "created_at": mocker.ANY,
                "room_id": str(self.living_room_id)
            }
        ]

    def test_get_entities_filtered(self, client, entities, mocker):
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
                "room_id": str(self.living_room_id)
            }
        ]

        response = client.get(f"/entities?room_id={self.kitchen_id}")
        assert response.status_code == 200
        assert response.json == [
            {
                "id": f"{uuid.UUID(int=1)}",
                "name": "Ceiling Light",
                "type": "light",
                "status": "off",
                "value": None,
                "created_at": mocker.ANY,
                "room_id": str(self.kitchen_id)
            }
        ]

        response = client.get("/entities?type=sensor&status=off")
        assert response.status_code == 200
        assert response.json == []
