import pytest
from django.db.models import F, Func
from mypy import api

from .test_decorator import OPTIONS


def safe_repr(value):
    if isinstance(value, Func):
        # Django's repr for expressions does not quote string parameters
        # Copy all expressions, wrapping their value in a "repr"
        value = value.copy()
        value.set_source_expressions(
            [
                expression.__class__(
                    repr(
                        expression.name
                        if isinstance(expression, F)
                        else expression.value
                    )
                )
                for expression in value.source_expressions
            ]
        )

    return repr(value)


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
    foo.{attribute} = {safe_repr(value)}
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
    @admin_display({attribute}={safe_repr(value)})
    def foo(self, obj: models.Model) -> int:
        return 1
    '''

    result = api.run(['-c', code])
    _, _, error_code = result
    assert error_code == 0, result
