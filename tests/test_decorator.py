import pytest
from django.contrib.admin import display as django_display
from django.db.models import F
from django.db.models.functions import Lower

from django_admin_display import admin_display, display

OPTIONS = [
    ('admin_order_field', 'radius'),
    ('admin_order_field', Lower(F('person_name'))),
    ('boolean', True),
    ('empty_value_display', 'Undefined'),
    ('short_description', 'Is big?'),
]

DISPLAY_OPTIONS = [
    ('ordering', 'admin_order_field', 'radius'),
    ('ordering', 'admin_order_field', Lower(F('person_name'))),
    ('boolean', 'boolean', True),
    ('empty_value', 'empty_value_display', 'Undefined'),
    ('description', 'short_description', 'Is big?'),
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


@pytest.mark.parametrize('parameter, attribute, value', DISPLAY_OPTIONS)
def test_display(parameter: str, attribute: str, value: object) -> None:
    @display(**{parameter: value})  # type: ignore[arg-type]
    def noop() -> None:
        pass

    assert getattr(noop, attribute) == value


@pytest.mark.parametrize(
    'parameter, value',
    [(parameter, value) for parameter, _, value in DISPLAY_OPTIONS],
)
def test_display_matches_django_builtin(parameter: str, value: object) -> None:
    @display(**{parameter: value})  # type: ignore[arg-type]
    def ours() -> None:
        pass

    @django_display(**{parameter: value})
    def builtin() -> None:
        pass

    assert vars(ours) == vars(builtin)


def test_display_rejects_boolean_and_empty_value() -> None:
    with pytest.raises(ValueError):

        @display(boolean=True, empty_value='Undefined')
        def noop() -> None:
            pass
