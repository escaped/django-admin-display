from collections.abc import Callable
from typing import TypeVar

from django.db.models.expressions import BaseExpression

ReturnType = TypeVar('ReturnType')
FuncType = Callable[..., ReturnType]
Func = TypeVar('Func', bound=FuncType)


def admin_display(
    admin_order_field: str | BaseExpression | None = None,
    boolean: bool | None = None,
    empty_value_display: str | None = None,
    short_description: str | None = None,
) -> Callable[[Func], Func]:
    """
    Extend method with special attributes for use by the django admin.
    """

    def wrapper(func: Func) -> Func:
        if admin_order_field is not None:
            setattr(func, 'admin_order_field', admin_order_field)
        if boolean is not None:
            setattr(func, 'boolean', boolean)
        if empty_value_display is not None:
            setattr(func, 'empty_value_display', empty_value_display)
        if short_description is not None:
            setattr(func, 'short_description', short_description)
        return func

    return wrapper
