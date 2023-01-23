# Changelog

All notable changes to this project will be documented in this file.

## [0.1.1] - 2023-01-23

### Added

- PATCH: add a route to handle patch request.
    - Added a basic Bearer Token to simulate a protected route
    - added more tests accordingly
    - Save the changes to db with SQLalchemy
- GET: added one route to get a single entity, based on entity_id
- Add GET param filters (`?type=xxxx`) on `/entities`
- Add some serializers to control allowed data sent by frontend, and a ResponseSerializer

### Changed

- Serializer: the `/entities` route returns the nested room into the object


