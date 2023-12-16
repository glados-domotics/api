import glados.repositories.rooms as repository


class TestRooms:

    def test_add(self, client):
        repository.add("Kitchen")

        room = repository.filter()[0]
        assert room.name == "Kitchen"
        assert room.created_at is not None

    def test_filter(self, client):
        assert repository.filter() == []

        room_names = ("Kitchen", "Living Room")
        repository.add(room_names[0])
        repository.add(room_names[1])

        rooms = repository.filter()
        assert len(rooms) == 2
        added_rooms_names = [room.name for room in rooms]
        assert room_names[0] in added_rooms_names
        assert room_names[1] in added_rooms_names

    def test_find(self, client):
        repository.add("Kitchen")

        kitchen = repository.filter()[0]
        room = repository.find(kitchen.id)
        assert room.name == "Kitchen"
        assert room.created_at is not None

    def test_update(self, client):
        repository.add("Kitchen")
        kitchen = repository.filter()[0]
        repository.update(kitchen.id, "Updated Kitchen")

        assert kitchen.name == "Updated Kitchen"
        assert kitchen.created_at is not None
