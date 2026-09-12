# django-admin-display

![PyPI](https://img.shields.io/pypi/v/django-admin-display?style=flat-square)
![GitHub Workflow Status (master)](https://img.shields.io/github/actions/workflow/status/escaped/django-admin-display/test.yml?branch=master&style=flat-square)
![Coveralls github branch](https://img.shields.io/coveralls/github/escaped/django-admin-display/master?style=flat-square)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/django-admin-display?style=flat-square)
![PyPI - License](https://img.shields.io/pypi/l/django-admin-display?style=flat-square)


Simplifies the use of function attributes (eg. `short_description`) for the django admin and makes mypy happy :)

**Note:** Django 3.2+ has [`@display`](https://docs.djangoproject.com/en/stable/ref/contrib/admin/#the-display-decorator) and [`@action`](https://docs.djangoproject.com/en/stable/ref/contrib/admin/actions/#the-action-decorator) decorators built-in.

## Requirements

* Python 3.10 or newer
* Django 5.2 or newer

The support range follows the upstream support policies: Django 5.2 is the oldest
release still receiving security support and Python 3.10 is the oldest Python
release supported by Django 5.2. See
[What Python version can I use with Django?](https://docs.djangoproject.com/en/stable/faq/install/#what-python-version-can-i-use-with-django)
and the [Python version status](https://devguide.python.org/versions/).

| Python | Django         |
|--------|----------------|
| 3.10   | 5.2            |
| 3.11   | 5.2            |
| 3.12   | 5.2, 6.0, 6.1  |
| 3.13   | 5.2, 6.0, 6.1  |
| 3.14   | 5.2, 6.0, 6.1  |

## Installation

```sh
pip install django-admin-display
```

## Usage

If you want to change the behaviour of how Django displays a read-only value in the admin interface,
you can add some [special attributes](https://docs.djangoproject.com/en/stable/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_display) to the corresponding method.
Supported values are

`short_description`  
    Customize the column’s title of the callable.

`empty_value_display`  
    Show this value instead, if the value of a field is `None`, an empty string, or an iterable without elements.

`admin_order_field`  
    Indicate that the value is represented by a certain database field. This can also be a
    [query expression](https://docs.djangoproject.com/en/stable/ref/models/expressions/).

`boolean`  
    Display a pretty “on” or “off” icon if the method returns a boolean.

The following example shows, how you normally apply these attributes to an `AdminModel` or a `Model` method.

```python
class Company(models.Model):
    ...

    def owner(self) -> bool:
        return self.owner.last_name

    owner.short_description = "Company owner"
    owner.admin_order_field = 'owner__last_name'
```

This module replaces the way of defining these attributes by providing a handy decorator.

```python
from django_admin_display import admin_display


class Company(models.Model):
    ...

    @admin_display(
        short_description="Company owner",
        admin_order_field='owner__last_name',
    )
    def owner(self) -> bool:
        return self.owner.last_name
```

## Why?

There are mainly two reasons why this module exists.

### Usage with `@property`

It is quite common that a calculated model property is displayed in the admin interface:

```python
class Company(models.Model):
    ...

    @property
    def created_on(self) -> datetime.date:
        return self.created_at.date()
```

In order to add special attributes, you have to create a protected method,
attach the attributes and wrap that method using `property()`:

```python
class Company(models.Model):
    ...

    def _created_on(self) -> datetime.date:
        return self.created_at.date()

    _created_on.short_description = "Created on"
    created_on = property(_created_on)
```

This is quite cumbersome, hard to read and most people don't know that this is even possible.
To overcome these downsides you can achieve the same result using the `@admin_display` decorator:

```python
from django_admin_display import admin_display


class Company(models.Model):
    ...

    @property
    @admin_display(
        short_description="Created on",
    )
    def created_on(self) -> datetime.date:
        return self.created_at.date()
```

### mypy

If you are using [mypy](http://mypy-lang.org/), you have probably stumbled over an error similar to this one

> "Callable[[Any, Any], Any]" has no attribute "short_description"

A common solution is to ignore the type checking by adding `# type: ignore` to the end of the line:

```python
class CompanyAdmin(admin.ModelAdmin):
    ...

    def created_on(self, company: models.Company) -> datetime.date:
        return company.created_at.date()

    created_on.short_description = "Created on"  # type: ignore
```

The issue is already known and heavily discussed on [github](https://github.com/python/mypy/issues/2087).

This decorator solves the issue by internally using `# type: ignore` and providing a well-defined signature for setting the attributes.
It is not an optimal solution but works well until the issue has been resolved.

## Development

This project uses [uv](https://docs.astral.sh/uv/) for packaging and dependency
management, [ruff](https://docs.astral.sh/ruff/) for linting and formatting,
[mypy](https://mypy-lang.org/) for static type checking and
[pytest](https://docs.pytest.org/) for tests.

Clone this repository and run

```sh
uv sync
```

to create a virtual environment containing all dependencies. Afterwards, you can run the test
suite using

```sh
uv run pytest
```

The test suite drives a real Django admin project (see `tests/`) end to end: it logs in
through the admin login form, renders the changelist, follows the sortable column headers
and submits the add form.

To lint and format the code, run

```sh
uv run ruff check --fix .
uv run ruff format .
```

and to type check the package and tests

```sh
uv run mypy django_admin_display tests
```

[pre-commit](https://pre-commit.com/) hooks are configured to run ruff before every
commit:

```sh
uvx pre-commit install
```

This repository follows the [Conventional Commits](https://www.conventionalcommits.org/)
style.
