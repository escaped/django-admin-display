import pytest
from django.db.models import F
from django.db.models.functions import Lower

from django_admin_display import admin_display

OPTIONS = [
    ('admin_order_field', 'radius'),
    ('admin_order_field', Lower(F('person_name'))),
    ('boolean', True),
    ('empty_value_display', 'Undefined'),
    ('short_description', 'Is big?'),
]


@pytest.mark.parametrize('attribute, value', OPTIONS)
def test_decorator(attribute: str, value: object) -> None:
    @admin_display(**{f'{attribute}': value})  # type: ignore[arg-type]
    def noop() -> None:
        pass

    assert hasattr(noop, attribute)
    assert getattr(noop, attribute) == value


def test_decorator__allow_tags_removed() -> None:
    with pytest.raises(TypeError):

        @admin_display(allow_tags=True)  # type: ignore[call-arg]
        def noop() -> None:
            pass
