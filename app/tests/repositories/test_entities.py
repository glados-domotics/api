import glados.repositories.entities as repository
from glados import constants


class TestEntities:

    def test_add(self, client):
        repository.add("Kitchen Lamp", constants.EntityType.light.name, constants.EntityStatus.on.name, None)

        entity = repository.filter()[0]
        assert entity.name == "Kitchen Lamp"
        assert entity.type == constants.EntityType.light.name
        assert entity.status == constants.EntityStatus.on.name
        assert entity.value is None

    def test_filter(self, client):
        assert repository.filter() == []

        repository.add("Kitchen Lamp", constants.EntityType.light.name, constants.EntityStatus.on.name, None)
        repository.add("Wall Switch", constants.EntityType.switch.name, constants.EntityStatus.on.name, "071010")
        entities = repository.filter()

        assert len(entities) == 2
        switch = list(filter(lambda x: x.value == "071010", entities))[0]
        assert switch.name == "Wall Switch"
        assert switch.type == constants.EntityType.switch.name
        assert switch.status == constants.EntityStatus.on.name
        assert switch.value == "071010"
        assert switch.room_id is None

    def test_find(self, client):
        repository.add("Kitchen Lamp", constants.EntityType.light.name, constants.EntityStatus.on.name, None)

        entity = repository.filter()[0]
        entity = repository.find(entity.id)
        assert entity.name == "Kitchen Lamp"

    def test_update(self, client):
        repository.add("Kitchen Lamp", constants.EntityType.light.name, constants.EntityStatus.on.name, None)

        entity = repository.filter()[0]
        entity = repository.update(entity.id, "Updated Kitchen Lamp", constants.EntityType.light.name, constants.EntityStatus.off.name, "Golden", None)
        assert entity.name == "Updated Kitchen Lamp"
        assert entity.type == constants.EntityType.light.name
        assert entity.status == constants.EntityStatus.off.name
        assert entity.value == "Golden"
        assert entity.room_id is None
