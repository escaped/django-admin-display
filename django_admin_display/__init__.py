from collections.abc import Callable
from typing import TypeVar

from django.db.models.expressions import BaseExpression

ReturnType = TypeVar('ReturnType')
FuncType = Callable[..., ReturnType]
Func = TypeVar('Func', bound=FuncType)


def display(
    *,
    boolean: bool | None = None,
    ordering: str | BaseExpression | None = None,
    description: str | None = None,
    empty_value: str | None = None,
) -> Callable[[Func], Func]:
    """
    Extend method with special attributes for use by the django admin.

    Mirrors the parameter names of Django's own ``django.contrib.admin.display``
    decorator, but is typed so the decorated method keeps its signature for mypy.
    """

    def wrapper(func: Func) -> Func:
        if boolean is not None and empty_value is not None:
            raise ValueError(
                "The boolean and empty_value arguments to the @display "
                "decorator are mutually exclusive.",
            )
        if boolean is not None:
            setattr(func, 'boolean', boolean)
        if ordering is not None:
            setattr(func, 'admin_order_field', ordering)
        if description is not None:
            setattr(func, 'short_description', description)
        if empty_value is not None:
            setattr(func, 'empty_value_display', empty_value)
        return func

    return wrapper


def admin_display(
    admin_order_field: str | BaseExpression | None = None,
    boolean: bool | None = None,
    empty_value_display: str | None = None,
    short_description: str | None = None,
) -> Callable[[Func], Func]:
    """
    Backwards-compatible wrapper for :func:`display` using the legacy parameter
    names of the django admin attributes.
    """
    return display(
        boolean=boolean,
        ordering=admin_order_field,
        description=short_description,
        empty_value=empty_value_display,
    )
