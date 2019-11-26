import pytest
from mypy import api

from .test_decorator import OPTIONS


@pytest.mark.parametrize('attribute, value', OPTIONS)
def test_failure(attribute, value):
    value = f'"{value}"' if isinstance(value, str) else value
    code = f'''
from django import admin
from django.db import models


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
    value = f'"{value}"' if isinstance(value, str) else value
    code = f'''
from django import admin
from django.db import models
from django_admin_display import admin_display


class SampleAdmin(admin.ModelAdmin):
    @admin_display({attribute}={value})
    def foo(self, obj: models.Model) -> int:
        return 1
    '''

    result = api.run(['-c', code])
    _, _, error_code = result
    assert error_code == 0, result
