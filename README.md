# django-admin-display

![Version](https://img.shields.io/pypi/v/django-admin-display.svg)
![Build status](https://travis-ci.org/escaped/django-admin-display.png?branch=master)
![Coverage](https://coveralls.io/repos/escaped/django-admin-display/badge.png?branch=master)
![Python Versions](https://img.shields.io/pypi/pyversions/django-admin-display.svg)
![License](https://img.shields.io/pypi/l/django-admin-display.svg)

Simplifies the use of function attributes (eg. `short_description`) for the django admin and makes mypy happy :)


## Requirements

- Python >= 3.6
- Django >= 1.11


## Usage

If you want to change the behaviour of how Django displays a read-only value in the admin interface,
you can add some [special attributes](>https://docs.djangoproject.com/en/2.1/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_display) to the corresponding method.
Supported values are

`short_description`  
    Customize the column’s title of the callable.
    
`empty_value_display`  
    Show this value instead, if the value of a field is `None`, an empty string, or an iterable without elements.
    
`admin_order_field`  
    Indicate that the value is represented by a certain database field.
    
`boolean`  
    Display a pretty “on” or “off” icon if the method returns a boolean.
    
`allow_tags` (deprecated since Django 1.9)  
    Disable auto-escaping.

The following example shows, how you normally apply these attributes to an `AdminModel` or a `Model` method.

    class Company(models.Model):
        ...

        def owner(self) -> bool:
            return self.owner.last_name
        is_valid.short_description = "Company owner"
        is_valid.admin_order_field = 'owner__last_name'

This module replaces the way of defining these attributes by providing a handy decorator.

    from django_admin_display import admin_display


    class Company(models.Model):
        ...

        @admin_display(
            short_description="Company owner",
            admin_order_field='owner__last_name',
        )
        def owner(self) -> bool:
            return self.owner.last_name


## Why?

There are mainly two reasons why this module exists.

### Usage with `@property`

It is quite common that a calculated model property is displayed in the admin interface:

    class Company(models.Model):
        ...

        @property
        def created_on(self) -> datetime.date:
            return self.created_at.date()

In order to add special attributes, you have to create a protected method,
attach the attributes and wrap that method using `property()`

    class Company(models.Model):
        ...

        def _created_on(self) -> datetime.date:
            return self.created_at.date()
        _created_on.short_description = "Created on"
        created_on = property(_created_on)

This is quite cumbersome, hard to read and most people don't know that this is even possible.
To overcome these downsides you can achieve the same result using the `@admin_diplay` decorator.

    from django_admin_display import admin_display


    class Company(models.Model):
        ...

        @property
        @admin_display(
            short_description = "Created on",
        )
        def created_on(self) -> datetime.date:
            return self.created_at.date()

### mypy

If you are using [mypy](http://mypy-lang.org/), you have probably stumbled over an error similar to this one

> "Callable[[Any, Any], Any]" has no attribute "short_description"

A common solution is to ignore the type checking by adding `# type: ignore` to the end of the line.

    class CompanyAdmin(admin.ModelAdmin):
        ...

        def created_on(self, company: models.Company) -> datetime.date:
            return company.created_at.date()
        created_on.short_description = "Created on"  # type: ignore

The issue is already known and heavily discussed on [github](https://github.com/python/mypy/issues/2087).

This decorator solves the issue by internally using `# type: ignore` and providing a well-defined signature for setting the attributes.
It is not an optimal solution but works well until the issue has been resolved.


## Development

This project is using [poetry](https://poetry.eustace.io/) to manage all
dev dependencies.
Clone this repository and run

      poetry install
      poetry run pip install Django

to create a virtual environment with all dependencies.
You can now run the test suite using

      poetry run pytest

This repository follows the [angular commit conventions](https://github.com/marionebl/commitlint/tree/master/@commitlint/config-angular).
