# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres
to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## `1.0.0` [!badge variant="info" text="NEXT"]

Expected: unknown

### Added

- [ ] Added validator
- [ ] Added serializer
- [ ] Added `min_length`, `max_length`, `choices`, `regex` options to `String` related types
- [ ] Added `gt`, `ge`, `lt`, `le` options to numeric types
- [ ] Added `Email` type
- [ ] Added `StructModel.__init__` hints for `IDE`

## `0.2.0` [!badge variant="info" text="LATEST"]

Released: 2023-10-22

### Added

### Changed

- [x] Upgraded to `Python 3.12`

### Removed

- [x] Removed unnecessary dependency: `ujson`

## `0.1.2`

Released: 2021-08-28

### Added

- [x] Added [`ujson`](https://github.com/ultrajson/ultrajson)

### Changed

- [x] Exposed `struct` and `byte_order` attributes of `StructModel`
- [x] Upgraded to `Python 3.10`

## `0.1.1`

Released: 2021-08-26

### Added

- [x] Added `UUID` type
- [x] Added `Decimal` type

### Fixed

- [x] Fixed invalid links
- [x] Fixed invalid python version

## `0.1.0`

Released: 2021-08-25

### Added

- [x] Project started