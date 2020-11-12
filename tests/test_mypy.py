import django
import pytest
from mypy import api

OPTIONS = [
    ('admin_order_field', '"radius"'),
    ('admin_order_field', 'Lower(F("person_name"))'),
    ('boolean', 'True'),
    ('empty_value_display', '"Undefined"'),
    ('short_description', '"Is big?"'),
]
if django.VERSION[:2] <= (1, 11):
    OPTIONS.append(('allow_tags', 'True'))


@pytest.mark.parametrize('attribute, value', OPTIONS)
def test_failure(attribute, value):
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
def test_success(attribute, value):
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
