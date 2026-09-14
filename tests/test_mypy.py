import pytest
from mypy import api

OPTIONS = [
    ('admin_order_field', '"radius"'),
    ('admin_order_field', 'Lower(F("person_name"))'),
    ('boolean', 'True'),
    ('empty_value_display', '"Undefined"'),
    ('short_description', '"Is big?"'),
]

DISPLAY_OPTIONS = [
    ('ordering', '"radius"'),
    ('ordering', 'Lower(F("person_name"))'),
    ('boolean', 'True'),
    ('empty_value', '"Undefined"'),
    ('description', '"Is big?"'),
]


@pytest.mark.parametrize('attribute, value', OPTIONS)
def test_failure(attribute: str, value: str) -> None:
    code = f'''
from django import admin
from django.db import models
from django.db.models import F
from django.db.models.functions import Lower


class SampleAdmin(admin.ModelAdmin):
    def foo(self, obj: models.Model) -> int:
        return 1
    foo.{attribute} = {value}
    '''

    result = api.run(['-c', code])
    _, _, error_code = result
    assert error_code > 0, result


@pytest.mark.parametrize('attribute, value', OPTIONS)
def test_success(attribute: str, value: str) -> None:
    code = f'''
from django import admin
from django.db import models
from django_admin_display import admin_display
from django.db.models import F
from django.db.models.functions import Lower


class SampleAdmin(admin.ModelAdmin):
    @admin_display({attribute}={value})
    def foo(self, obj: models.Model) -> int:
        return 1
    '''

    result = api.run(['-c', code])
    _, _, error_code = result
    assert error_code == 0, result


@pytest.mark.parametrize('parameter, value', DISPLAY_OPTIONS)
def test_display_success(parameter: str, value: str) -> None:
    code = f'''
from django import admin
from django.db import models
from django_admin_display import display
from django.db.models import F
from django.db.models.functions import Lower


class SampleAdmin(admin.ModelAdmin):
    @display({parameter}={value})
    def foo(self, obj: models.Model) -> int:
        return 1
    '''

    result = api.run(['-c', code])
    _, _, error_code = result
    assert error_code == 0, result


def test_display_preserves_types() -> None:
    code = '''
from django_admin_display import display


@display(ordering="radius")
def foo(a: int) -> str:
    return str(a)


reveal_type(foo)
    '''

    result = api.run(['-c', code])
    stdout, _, error_code = result
    assert error_code == 0, result
    assert 'def (a: int) -> str' in stdout, result
