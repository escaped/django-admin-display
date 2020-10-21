import django
import pytest
from django.db.models import F
from django.db.models.functions import Lower

from django_admin_display import admin_display

requires_django2 = pytest.mark.skipif(
    django.VERSION[:2] <= (1, 11), reason='django < 2.0 is required'
)

OPTIONS = [
    ('admin_order_field', 'radius'),
    ('admin_order_field', Lower(F('person_name'))),
    ('boolean', True),
    ('empty_value_display', 'Undefined'),
    ('short_description', 'Is big?'),
]
if django.VERSION[:2] <= (1, 11):
    OPTIONS.append(('allow_tags', True))


@pytest.mark.parametrize('attribute, value', OPTIONS)
def test_decorator(attribute, value):
    @admin_display(**{f'{attribute}': value})
    def noop():
        pass

    assert hasattr(noop, attribute)
    assert getattr(noop, attribute) == value


@requires_django2
def test_decorator__legacy_attribute():
    with pytest.raises(AttributeError):

        @admin_display(allow_tags=True)
        def noop():
            pass
