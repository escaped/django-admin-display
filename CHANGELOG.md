# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- End-to-end tests that drive the real Django admin UI: login form, changelist
  rendering, sortable column headers and the add form, asserting on DOM and
  database state.

### Changed

- **BREAKING:** Dropped support for Python 3.6–3.9, which are all end-of-life.
  The package now requires Python 3.10 or newer.
- **BREAKING:** Dropped support for Django 1.11–5.1, which are all end-of-life.
  The package now requires Django 5.2 or newer.
- Migrated packaging and tooling from Poetry, tox, black, isort and flake8 to
  uv, hatchling and ruff. CI now tests the full supported Python × Django
  matrix.

### Removed

- **BREAKING:** The `allow_tags` argument of `admin_display` was removed.
  Django removed `allow_tags` in 3.0, so it could only raise on any version
  this package supports.
- The cruft template auto-updater and its scheduled workflow.

## [1.3.0] - 11.11.2020

### Added

- Support BaseExpression on admin_order_field, @brianhelba

## [1.2.0] - 19.09.2020

### Added

- Add support for python 3.8
- Add support for Django 3.1

### Fixed

- add py.typed for mypy support

## [1.1.0] - 18.02.2019

### Fixed

- Fix mypy compatibility

## [1.0.0] - 12.02.2019

### Added

- Initial release

[Unreleased]: https://github.com/escaped/django-admin-display/compare/1.3.0...HEAD
[1.3.0]: https://github.com/escaped/django-admin-display/compare/1.2.0...1.3.0
[1.2.0]: https://github.com/escaped/django-admin-display/compare/1.1.0...1.2.0
[1.1.0]: https://github.com/escaped/django-admin-display/releases/tag/1.1.0
